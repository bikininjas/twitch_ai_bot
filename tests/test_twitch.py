"""
Test de connexion pour Twitch IRC
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent.parent / "src"))

import asyncio
import logging
from twitch_connection.auth import TwitchAuth
from twitch_connection.message_handler import TwitchMessageHandler


def test_twitch_connection():
    """Test la connexion à l'API Twitch"""
    print("🎮 Test de connexion à Twitch...")

    try:
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)

        # Test de l'authentification
        print("🔐 Test de l'authentification...")
        auth = TwitchAuth()
        if auth.validate_credentials():
            print("✅ Identifiants Twitch valides")
            token, client_id, channel, bot_name = auth.get_credentials()
            print(f"📺 Canal: {channel}")
            print(f"🤖 Nom du bot: {bot_name}")
        else:
            print("❌ Identifiants Twitch invalides")
            return False

        # Test d'initialisation du gestionnaire
        print("📡 Test d'initialisation du gestionnaire...")
        message_handler = TwitchMessageHandler()

        # Callback de test pour les messages
        def test_message_callback(username, message):
            print(f"📨 Message reçu de {username}: {message}")

        message_handler.initialize_bot(message_callback=test_message_callback)
        print("✅ Gestionnaire Twitch initialisé")

        # Test de statut de connexion
        print("🔍 Vérification du statut...")
        status = message_handler.get_connection_status()
        print(f"📊 Statut de connexion: {status}")

        print("🎉 Tous les tests Twitch ont réussi!")
        print("⚠️  Note: Pour tester la connexion complète, lancez le bot principal")
        return True

    except Exception as e:
        print(f"❌ Erreur lors du test Twitch: {e}")
        return False


if __name__ == "__main__":
    success = test_twitch_connection()
    if not success:
        sys.exit(1)
    print("✅ Test Twitch terminé avec succès")
