#!/usr/bin/env python3
"""Synchronise les personnalités JSON locales vers SQLite Cloud.

Usage rapide:
    python scripts/sync_personalities_to_db.py

Le script lit les variables d'environnement suivantes (chargées via `.env`):
    PERSONALITY_DB_URL                -> obligatoire
    PERSONALITY_DB_TABLE              -> optionnel (défaut: personalities)
    PERSONALITY_DB_TYPE_COLUMN        -> optionnel (défaut: type)
    PERSONALITY_DB_PAYLOAD_COLUMN     -> optionnel (défaut: payload)

Le script crée la table si nécessaire et insère/actualise les personnalités en utilisant
le contenu JSON des fichiers présents dans `src/gemini_ai/personalities/`.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

# sqlitecloud est optionnel dans l'application, mais requis pour ce script.
try:
    import sqlitecloud  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Le module sqlitecloud est requis. Installez-le via 'pip install sqlitecloud'."
    ) from exc

# Configuration du logging console
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
LOGGER = logging.getLogger("personality_sync")

PERSONALITIES_DIR = (
    Path(__file__).resolve().parent.parent / "src" / "gemini_ai" / "personalities"
)


def load_personality_files() -> Dict[str, dict]:
    """Charge tous les fichiers JSON de personnalités dans un dict {type: payload}."""
    if not PERSONALITIES_DIR.exists():
        raise FileNotFoundError(
            f"Dossier des personnalités introuvable: {PERSONALITIES_DIR}"
        )

    personalities: Dict[str, dict] = {}
    for file_path in sorted(PERSONALITIES_DIR.glob("*.json")):
        persona_type = file_path.stem
        with file_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        personalities[persona_type] = payload
        LOGGER.debug("Chargé %s depuis %s", persona_type, file_path.name)

    if not personalities:
        raise RuntimeError("Aucune personnalité trouvée dans le dossier local.")

    LOGGER.info("%d personnalités chargées depuis les JSON locaux", len(personalities))
    return personalities


def ensure_table(
    connection: sqlitecloud.Connection,
    table: str,
    type_column: str,
    payload_column: str,
) -> None:
    """Crée la table cible si nécessaire."""
    ddl = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        {type_column} TEXT PRIMARY KEY,
        {payload_column} JSON NOT NULL
    )
    """
    connection.execute(ddl)
    LOGGER.info("Table '%s' prête.", table)


def sync(
    connection: sqlitecloud.Connection,
    table: str,
    type_column: str,
    payload_column: str,
    data: Dict[str, dict],
) -> None:
    """Synchronise les personnalités vers la base (INSERT OR REPLACE)."""
    insert_sql = (
        f"INSERT OR REPLACE INTO {table} ({type_column}, {payload_column}) "
        f"VALUES (?, json(?))"
    )

    rows = 0
    for persona_type, payload in data.items():
        payload_json = json.dumps(payload, ensure_ascii=False)
        params: tuple[Any, ...] = (persona_type, payload_json)
        connection.execute(insert_sql, params)
        rows += 1
        LOGGER.debug("Synchronisé %s", persona_type)

    LOGGER.info("%d personnalités synchronisées dans %s", rows, table)


def main() -> None:
    load_dotenv()

    connection_string = os.getenv("PERSONALITY_DB_URL")
    if not connection_string:
        raise SystemExit(
            "PERSONALITY_DB_URL est manquant. Ajoutez-le à votre fichier .env ou exportez-le."
        )

    table = os.getenv("PERSONALITY_DB_TABLE", "personalities")
    type_column = os.getenv("PERSONALITY_DB_TYPE_COLUMN", "type")
    payload_column = os.getenv("PERSONALITY_DB_PAYLOAD_COLUMN", "payload")

    LOGGER.info("Connexion à SQLite Cloud...")
    connection = sqlitecloud.connect(connection_string)

    try:
        ensure_table(connection, table, type_column, payload_column)
        personalities = load_personality_files()
        sync(connection, table, type_column, payload_column, personalities)
        LOGGER.info("Synchronisation terminée avec succès.")
    finally:
        connection.close()
        LOGGER.info("Connexion fermée.")


if __name__ == "__main__":
    main()
