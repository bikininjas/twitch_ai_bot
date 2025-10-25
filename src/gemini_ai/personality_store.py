"""Abstractions de stockage pour les personnalités Nova.

Permet de charger les configurations de personnalités depuis différents backends
(JSON local par défaut, SQLite Cloud facultatif).
"""

from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, Optional

from .personality_schema import PersonalityConfig

logger = logging.getLogger(__name__)


class BasePersonalityStore(ABC):
    """Contrat minimal pour un backend de personnalités."""

    @abstractmethod
    def load(self) -> Dict[str, PersonalityConfig]:
        """Retourne un dictionnaire {type: PersonalityConfig}."""
        raise NotImplementedError


class JsonPersonalityStore(BasePersonalityStore):
    """Charge les personnalités depuis le dossier JSON historique."""

    def __init__(self, personalities_dir: Optional[str] = None):
        self.personalities_dir = personalities_dir or os.path.join(
            os.path.dirname(__file__), "personalities"
        )

    def load(self) -> Dict[str, PersonalityConfig]:
        personalities: Dict[str, PersonalityConfig] = {}

        if not os.path.exists(self.personalities_dir):
            logger.error(
                "Dossier des personnalités introuvable: %s",
                self.personalities_dir,
            )
            return personalities

        for filename in sorted(os.listdir(self.personalities_dir)):
            if not filename.endswith(".json"):
                continue

            personality_type = filename[:-5]
            file_path = os.path.join(self.personalities_dir, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as handle:
                    raw_data = json.load(handle)

                config = PersonalityConfig(**raw_data)
                personalities[personality_type] = config
                logger.debug(
                    "[JSON] Personnalité chargée: %s (type=%s)",
                    config.name,
                    personality_type,
                )
            except Exception as exc:  # pragma: no cover - log et continuer
                logger.error(
                    "Erreur lors du chargement du fichier %s: %s",
                    filename,
                    exc,
                )
                continue

        return personalities


class SQLitePersonalityStore(BasePersonalityStore):
    """Charge les personnalités depuis une base SQLite Cloud."""

    def __init__(
        self,
        connection_string: str,
        table: str = "personalities",
        type_column: str = "type",
        payload_column: str = "payload",
    ) -> None:
        if not connection_string:
            raise ValueError("Le connection string SQLite Cloud est requis")

        self.connection_string = connection_string
        self.table = table
        self.type_column = type_column
        self.payload_column = payload_column

    def load(self) -> Dict[str, PersonalityConfig]:
        try:
            import sqlitecloud  # type: ignore
        except ImportError as exc:  # pragma: no cover - dépendance optionnelle
            raise RuntimeError(
                "Le module sqlitecloud est requis pour utiliser le backend SQLite"
            ) from exc

        personalities: Dict[str, PersonalityConfig] = {}
        connection = None
        try:
            connection = sqlitecloud.connect(self.connection_string)
            query = (
                f"SELECT {self.type_column}, {self.payload_column} "
                f"FROM {self.table}"
            )
            cursor = connection.execute(query)

            for row in cursor.fetchall():
                persona_type = row[0]
                payload = row[1]

                if not persona_type or payload is None:
                    logger.debug(
                        "[SQLite] Ligne ignorée (type ou payload vide): %s", row
                    )
                    continue

                config = self._to_config(payload)
                personalities[str(persona_type)] = config
                logger.debug(
                    "[SQLite] Personnalité chargée: %s (type=%s)",
                    config.name,
                    persona_type,
                )

            logger.info(
                "Chargé %d personnalités depuis SQLite Cloud (table=%s)",
                len(personalities),
                self.table,
            )
            return personalities
        except Exception as exc:
            raise RuntimeError(
                f"Erreur lors de la récupération des personnalités SQLite: {exc}"
            ) from exc
        finally:
            if connection is not None:
                try:
                    connection.close()
                except Exception as close_exc:  # pragma: no cover
                    logger.warning("Erreur lors de la fermeture SQLite: %s", close_exc)

    def _to_config(self, payload) -> PersonalityConfig:
        if isinstance(payload, (bytes, bytearray)):
            payload = payload.decode("utf-8")

        if isinstance(payload, str):
            data = json.loads(payload)
        elif isinstance(payload, dict):
            data = payload
        else:
            raise ValueError(
                f"Format de payload non supporté pour une personnalité: {type(payload)}"
            )

        return PersonalityConfig(**data)


def build_store(storage_options: Optional[dict] = None) -> BasePersonalityStore:
    """Fabrique le store approprié à partir des options fournies."""
    storage_options = storage_options or {}
    connection_string = storage_options.get("personality_db_url")

    if connection_string:
        table = storage_options.get("personality_db_table", "personalities")
        type_column = storage_options.get("personality_db_type_column", "type")
        payload_column = storage_options.get("personality_db_payload_column", "payload")

        try:
            return SQLitePersonalityStore(
                connection_string=connection_string,
                table=table,
                type_column=type_column,
                payload_column=payload_column,
            )
        except Exception as exc:
            logger.error(
                "Impossible d'initialiser le backend SQLite Cloud (%s). "
                "Retour au stockage JSON.",
                exc,
            )

    return JsonPersonalityStore()
