"""
Point d'entrée principal du bot Twitch AI
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent))

from utils.config import (
    setup_logging,
    load_config,
    validate_config,
    get_startup_message,
)
from twitch_connection.auth import TwitchAuth
from twitch_connection.message_handler import TwitchMessageHandler
from gemini_ai.ai_handler import GeminiHandler
from chat_handler.chat_manager import ChatHandler


class TwitchAIBot:
    """Bot Twitch principal avec IA Gemini"""

    def __init__(self):
        """Initialise le bot principal"""
        self.config = None
        self.logger = None
        self.twitch_handler = None
        self.ai_handler = None
        self.chat_handler = None
        self.running = False

        # Gestionnaire de signaux pour arrêt propre
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def initialize(self) -> bool:
        """
        Initialise tous les composants du bot

        Returns:
            bool: True si l'initialisation réussit
        """
        try:
            # Charger la configuration
            self.config = load_config()
            if not validate_config(self.config):
                print("❌ Configuration invalide. Vérifiez votre fichier .env")
                return False

            # Configurer le logging
            self.logger = setup_logging(
                log_level=self.config["logging"]["level"],
                log_dir=self.config["logging"]["dir"],
            )

            # Afficher le message de démarrage
            print(get_startup_message())
            self.logger.info("Démarrage du bot Twitch AI")

            # Initialiser les gestionnaires
            if not self._initialize_handlers():
                return False

            self.logger.info("✅ Bot initialisé avec succès")
            return True

        except Exception as e:
            if self.logger:
                self.logger.error(f"Erreur lors de l'initialisation: {e}")
            else:
                print(f"❌ Erreur lors de l'initialisation: {e}")
            return False

    def _initialize_handlers(self) -> bool:
        """
        Initialise tous les gestionnaires

        Returns:
            bool: True si tous les gestionnaires sont initialisés
        """
        try:
            # Gestionnaire IA Gemini
            self.logger.info("🧠 Initialisation du gestionnaire Gemini AI...")
            self.ai_handler = GeminiHandler()
            if not self.ai_handler.initialize():
                self.logger.error("❌ Échec de l'initialisation Gemini")
                return False
            self.logger.info("✅ Gemini AI initialisé")

            # Gestionnaire Twitch
            self.logger.info("🎮 Initialisation du gestionnaire Twitch...")
            self.twitch_handler = TwitchMessageHandler()
            self.twitch_handler.initialize_bot(
                message_callback=self._on_message_received
            )
            self.logger.info("✅ Gestionnaire Twitch initialisé")

            # Gestionnaire de chat
            self.logger.info("💬 Initialisation du gestionnaire de chat...")
            self.chat_handler = ChatHandler(self.ai_handler, self.twitch_handler)
            if not self.chat_handler.initialize():
                self.logger.error(
                    "❌ Échec de l'initialisation du gestionnaire de chat"
                )
                return False
            self.logger.info("✅ Gestionnaire de chat initialisé")

            return True

        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation des gestionnaires: {e}")
            return False

    async def _on_message_received(self, username: str, message: str):
        """
        Callback appelé lors de la réception d'un message Twitch

        Args:
            username: Nom de l'utilisateur
            message: Contenu du message
        """
        try:
            if self.chat_handler:
                await self.chat_handler.handle_incoming_message(username, message)
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement du message: {e}")

    async def start(self):
        """Démarre le bot"""
        if not self.chat_handler or not self.twitch_handler:
            self.logger.error("Bot non initialisé")
            return

        try:
            self.logger.info("🚀 Démarrage du bot...")

            # Démarrer le gestionnaire de chat
            if not await self.chat_handler.start():
                self.logger.error("❌ Échec du démarrage du gestionnaire de chat")
                return

            # Connecter à Twitch
            self.logger.info("🔌 Connexion à Twitch...")
            await self.twitch_handler.connect()

            self.running = True
            self.logger.info("✅ Bot démarré avec succès!")

            # Envoyer un message de test si configuré
            await self._send_startup_message()

            # Maintenir le bot en vie
            await self._keep_alive()

        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage: {e}")
            await self.stop()

    async def _send_startup_message(self):
        """Envoie un message de démarrage avec personnalité dans le chat"""
        try:
            if self.chat_handler:
                startup_msg = (
                    await self.chat_handler.get_startup_personality_announcement()
                )
                await self.twitch_handler.send_message(startup_msg)
                self.logger.info(f"Message de démarrage envoyé: {startup_msg}")
            else:
                fallback_msg = (
                    "🤖 nova_the_red_cat est connecté ! Prêt à être sarcastique... 😏"
                )
                await self.twitch_handler.send_message(fallback_msg)

        except Exception as e:
            self.logger.warning(f"Impossible d'envoyer le message de démarrage: {e}")

    async def _keep_alive(self):
        """Maintient le bot en vie"""
        while self.running:
            try:
                # Vérification périodique du statut
                await asyncio.sleep(30)
                self._log_status()

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Erreur dans la boucle principale: {e}")
                await asyncio.sleep(5)

    def _log_status(self):
        """Log le statut périodique du bot"""
        try:
            if self.chat_handler:
                status = self.chat_handler.get_status()
                self.logger.debug(f"Statut bot: {status}")
        except Exception as e:
            self.logger.error(f"Erreur lors du log de statut: {e}")

    async def stop(self):
        """Arrête le bot proprement"""
        try:
            self.logger.info("🛑 Arrêt du bot...")
            self.running = False

            if self.chat_handler:
                self.chat_handler.stop()

            if self.twitch_handler:
                self.twitch_handler.disconnect()

            self.logger.info("✅ Bot arrêté proprement")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'arrêt: {e}")

    def _signal_handler(self, signum, frame):
        """Gestionnaire de signaux pour arrêt propre"""
        print(f"\\n🛑 Signal {signum} reçu. Arrêt du bot...")
        if self.running:
            asyncio.create_task(self.stop())
        sys.exit(0)


async def main():
    """Fonction principale"""
    bot = TwitchAIBot()

    if not bot.initialize():
        print("❌ Impossible d'initialiser le bot")
        sys.exit(1)

    try:
        await bot.start()
    except KeyboardInterrupt:
        print("\\n🛑 Interruption utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
    finally:
        await bot.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n👋 Au revoir!")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)
