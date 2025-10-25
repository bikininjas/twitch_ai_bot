"""Suite de tests d'authentification pour Twitch, Gemini et la base SQLite Cloud."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ajouter src/ au PYTHONPATH pour les imports locaux
sys.path.append(str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv  # type: ignore

from twitch_connection.auth import TwitchAuth  # type: ignore
from gemini_ai.config import GeminiConfig  # type: ignore
from gemini_ai.ai_handler import GeminiHandler  # type: ignore
from gemini_ai.personality_store import SQLitePersonalityStore  # type: ignore


def test_twitch_authentication() -> bool:
    """Valide la présence et la forme des identifiants Twitch."""
    print("🎮 Vérification des identifiants Twitch...")
    try:
        auth = TwitchAuth()
    except Exception as exc:
        print(f"❌ Impossible de charger l'authentification Twitch: {exc}")
        return False

    if auth.validate_credentials():
        token, client_id, channel, bot_name = auth.get_credentials()
        print("✅ Identifiants valides")
        print(f"   • Canal: {channel}")
        print(f"   • Bot: {bot_name}")
        print(f"   • Token: {token[:6]}… ({len(token)} caractères)")
        print(f"   • Client ID: {client_id[:6]}… ({len(client_id)} caractères)")
        return True

    print("❌ Identifiants Twitch invalides ou incomplets")
    return False


def test_gemini_authentication() -> bool:
    """Teste la connexion à l'API Gemini."""
    print("🧠 Vérification de l'accès Gemini AI...")
    try:
        config = GeminiConfig()
        print("✅ Configuration Gemini chargée")
    except Exception as exc:
        print(f"❌ Impossible de charger la configuration Gemini: {exc}")
        return False

    try:
        if not config.test_connection():
            print("❌ Échec du ping API Gemini")
            return False
        print("✅ Ping API Gemini réussi")
    except Exception as exc:
        print(f"❌ Erreur lors du test de connexion Gemini: {exc}")
        return False

    handler = GeminiHandler()
    if not handler.initialize():
        print("❌ Gestionnaire Gemini impossible à initialiser")
        return False

    print("✅ Gestionnaire Gemini opérationnel")
    return True


def test_database_connection() -> bool:
    """Teste la connexion à SQLite Cloud et la disponibilité de la table."""
    print("🗄️ Vérification de la base SQLite Cloud...")
    load_dotenv()

    connection_string = os.getenv("PERSONALITY_DB_URL")
    if not connection_string:
        print("❌ PERSONALITY_DB_URL manquant dans l'environnement")
        return False

    table = os.getenv("PERSONALITY_DB_TABLE", "personalities")
    type_column = os.getenv("PERSONALITY_DB_TYPE_COLUMN", "type")
    payload_column = os.getenv("PERSONALITY_DB_PAYLOAD_COLUMN", "payload")

    try:
        store = SQLitePersonalityStore(
            connection_string=connection_string,
            table=table,
            type_column=type_column,
            payload_column=payload_column,
        )
        personalities = store.load()
    except Exception as exc:
        print(f"❌ Impossible de charger les personnalités depuis SQLite Cloud: {exc}")
        return False

    if not personalities:
        print("❌ Aucune personnalité trouvée dans la base")
        return False

    print(f"✅ {len(personalities)} personnalités disponibles dans SQLite Cloud")
    return True


def run_tests() -> bool:
    """Exécute l'ensemble des tests d'authentification."""
    load_dotenv()

    tests = [
        ("Twitch", test_twitch_authentication),
        ("Gemini", test_gemini_authentication),
        ("SQLite Cloud", test_database_connection),
    ]

    results = []
    for label, fn in tests:
        print("\n" + "=" * 60)
        print(f"🔍 Test {label}")
        print("=" * 60)
        try:
            result = fn()
        except Exception as exc:  # pragma: no cover - diagnostic lisible
            print(f"❌ Exception inattendue pendant le test {label}: {exc}")
            result = False
        results.append(result)

    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ AUTHENTIFICATION")
    print("=" * 60)
    overall = True
    for (label, _), result in zip(tests, results):
        status = "✅ OK" if result else "❌ KO"
        print(f"{label:>12}: {status}")
        overall = overall and result

    if overall:
        print("\n🎉 Toutes les authentifications sont opérationnelles !")
    else:
        print("\n❌ Une ou plusieurs authentifications ont échoué")
    return overall


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
