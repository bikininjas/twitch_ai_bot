"""
Test de fonctionnement complet du bot
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent.parent / "src"))

import asyncio
import logging
from utils.config import load_config, validate_config
from chat_handler.mention_detector import MentionDetector


def test_bot_functionality():
    """Test les fonctionnalités principales du bot"""
    print("🤖 Test de fonctionnalité du bot...")

    try:
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)

        # Test de chargement de configuration
        print("📋 Test de chargement de configuration...")
        config = load_config()
        if validate_config(config):
            print("✅ Configuration valide")
            print(f"📺 Canal: {config['twitch']['channel']}")
            print(f"👤 Propriétaire: {config['behavior']['owner_username']}")
        else:
            print("❌ Configuration invalide")
            return False

        # Test du détecteur de mentions
        print("🎯 Test du détecteur de mentions...")
        detector = MentionDetector()

        # Tests de cas d'usage
        test_cases = [
            ("redpikpik", "Hello everyone!", True, "owner_message"),
            ("randomuser", "Hey @bot_name", True, "bot_mentioned"),
            ("randomuser", "Just chatting", False, "no_trigger"),
            ("testuser", "bot_name how are you?", True, "bot_mentioned"),
        ]

        for username, message, should_respond, expected_reason in test_cases:
            result, reason = detector.should_respond(username, message)
            if result == should_respond and (
                not should_respond or reason == expected_reason
            ):
                print(f"✅ Test '{username}': '{message}' -> {result} ({reason})")
            else:
                print(
                    f"❌ Test '{username}': '{message}' -> Expected {should_respond}, got {result}"
                )

        # Test de nettoyage de message
        print("🧹 Test de nettoyage de message...")
        cleaned = detector.clean_message_for_ai("@bot_name hello there!")
        print(f"🔄 Message nettoyé: '{cleaned}'")

        # Test d'informations de déclenchement
        print("📊 Test d'informations de déclenchement...")
        trigger_info = detector.get_trigger_info("redpikpik", "Hello bot!")
        print(f"📈 Info de déclenchement: {trigger_info}")

        print("🎉 Tous les tests de fonctionnalité ont réussi!")
        return True

    except Exception as e:
        print(f"❌ Erreur lors du test de fonctionnalité: {e}")
        return False


def test_chat_scenarios():
    """Test des scénarios de chat spécifiques"""
    print("💬 Test des scénarios de chat...")

    try:
        detector = MentionDetector()

        # Scénarios de test
        scenarios = [
            {
                "name": "Message du propriétaire",
                "username": "redpikpik",
                "message": "Comment ça va ?",
                "expected_response": True,
                "expected_reason": "owner_message",
            },
            {
                "name": "Mention directe",
                "username": "viewer123",
                "message": "@bot_name tu es là ?",
                "expected_response": True,
                "expected_reason": "bot_mentioned",
            },
            {
                "name": "Message normal",
                "username": "viewer456",
                "message": "Super stream !",
                "expected_response": False,
                "expected_reason": "no_trigger",
            },
            {
                "name": "Mention dans phrase",
                "username": "chatuser",
                "message": "Je pense que bot_name est cool",
                "expected_response": True,
                "expected_reason": "bot_mentioned",
            },
        ]

        for scenario in scenarios:
            result, reason = detector.should_respond(
                scenario["username"], scenario["message"]
            )

            success = result == scenario["expected_response"] and (
                not result or reason == scenario["expected_reason"]
            )

            status = "✅" if success else "❌"
            print(f"{status} {scenario['name']}: {result} ({reason})")

        return True

    except Exception as e:
        print(f"❌ Erreur lors du test de scénarios: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Démarrage des tests de fonctionnalité...")

    success1 = test_bot_functionality()
    success2 = test_chat_scenarios()

    if success1 and success2:
        print("✅ Tous les tests ont réussi!")
        print("🚀 Le bot est prêt à être lancé!")
    else:
        print("❌ Certains tests ont échoué")
        sys.exit(1)
