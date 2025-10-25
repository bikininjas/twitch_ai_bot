"""
Gestionnaire principal pour toutes les interactions de chat
"""

import logging
import asyncio
from typing import Optional
from .mention_detector import MentionDetector
from .message_processor import MessageProcessor
from twitch_connection.event_handler import TwitchEventHandler, TwitchEventListener

logger = logging.getLogger(__name__)


class ChatHandler:
    """Gestionnaire principal pour le système de chat"""

    def __init__(self, ai_handler, twitch_handler):
        """
        Initialise le gestionnaire de chat

        Args:
            ai_handler: Instance du gestionnaire IA (Gemini)
            twitch_handler: Instance du gestionnaire Twitch
        """
        self.ai_handler = ai_handler
        self.twitch_handler = twitch_handler
        self.mention_detector = MentionDetector()
        self.message_processor = None
        self.is_active = False

        # Gestionnaire d'événements pour changements de personnalité
        self.event_handler = TwitchEventHandler(self._on_personality_change_event)
        self.event_listener = TwitchEventListener(
            self.event_handler, self._send_message_callback
        )

        logger.info("Gestionnaire de chat initialisé")

    def initialize(self) -> bool:
        """
        Initialise tous les composants du gestionnaire de chat

        Returns:
            bool: True si l'initialisation réussit
        """
        try:
            # Initialiser le processeur de messages avec callback
            self.message_processor = MessageProcessor(
                ai_handler=self.ai_handler,
                response_callback=self._send_message_callback,
            )

            # Configurer la référence croisée pour les commandes spéciales
            self.message_processor.set_chat_handler_reference(self)

            logger.info("Gestionnaire de chat initialisé avec succès")
            return True

        except Exception as e:
            logger.error(
                f"Erreur lors de l'initialisation du gestionnaire de chat: {e}"
            )
            return False

    async def _send_message_callback(self, message: str):
        """
        Callback pour envoyer des messages via Twitch

        Args:
            message: Message à envoyer
        """
        try:
            if self.twitch_handler:
                await self.twitch_handler.send_message(message)
            else:
                logger.error(
                    "Gestionnaire Twitch non disponible pour envoyer le message"
                )
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message: {e}")

    async def handle_incoming_message(self, username: str, message: str):
        """
        Gère un message entrant depuis Twitch

        Args:
            username: Nom de l'utilisateur
            message: Contenu du message
        """
        if not self.is_active or not self.message_processor:
            logger.warning("Gestionnaire de chat non actif")
            return

        try:
            # Traiter le message immédiatement
            await self.message_processor.process_message(username, message)

            # Analyser le message pour des événements (follow, sub, etc.)
            # Créer un objet message factice pour l'event listener
            class FakeMessage:
                def __init__(self, content, author_name):
                    self.content = content
                    self.author = type("Author", (), {"name": author_name})()

            fake_msg = FakeMessage(message, username)
            await self.event_listener.on_message(fake_msg)

        except Exception as e:
            logger.error(f"Erreur lors du traitement du message entrant: {e}")

    async def _on_personality_change_event(
        self, event_type: str, force: bool = False
    ) -> Optional[str]:
        """
        Callback appelé lors d'un événement qui doit changer la personnalité

        Args:
            event_type: Type d'événement qui a déclenché le changement
            force: Ignorer le cooldown

        Returns:
            str: Message d'annonce du changement de personnalité ou None si en cooldown
        """
        try:
            if self.ai_handler:
                # Changer la personnalité et obtenir l'annonce
                announcement = self.ai_handler.change_personality(force=force)
                if announcement:
                    logger.info(
                        f"Personnalité changée suite à l'événement: {event_type}"
                    )
                    return announcement
                else:
                    logger.debug(
                        f"Changement de personnalité ignoré (cooldown) pour: {event_type}"
                    )
                    return None
            else:
                return (
                    "🤖 Quelque chose d'excitant s'est passé, mais je suis confus ! 🤯"
                )

        except Exception as e:
            logger.error(
                f"Erreur lors du changement de personnalité pour événement {event_type}: {e}"
            )
            return "🤖 J'ai essayé de changer de personnalité mais j'ai bugué ! 💥"

    async def start(self):
        """Démarre le gestionnaire de chat"""
        if not self.message_processor:
            logger.error("Gestionnaire de chat non initialisé")
            return False

        try:
            self.is_active = True
            logger.info("Gestionnaire de chat démarré")

            # Démarrer le traitement de la queue en arrière-plan
            asyncio.create_task(self.message_processor.start_processing_queue())

            return True

        except Exception as e:
            logger.error(f"Erreur lors du démarrage du gestionnaire de chat: {e}")
            self.is_active = False
            return False

    async def get_startup_personality_announcement(self) -> str:
        """
        Génère le message d'annonce de personnalité au démarrage

        Returns:
            str: Message d'annonce avec personnalité actuelle
        """
        try:
            if self.ai_handler:
                # Récupérer le nom de la personnalité actuelle
                personality_name = self.ai_handler.get_current_personality_name()

                # Obtenir l'annonce de personnalité (sans changer, juste récupérer l'actuelle)
                try:
                    current_personality = (
                        self.ai_handler.response_generator.personality_manager.current_personality
                    )
                    if current_personality:
                        # Choisir une variante aléatoire pour le démarrage
                        import random

                        announcement_variant = random.choice(
                            current_personality.announcement_variants
                        )
                        return f"🤖 {personality_name} est connecté ! {announcement_variant}"
                    else:
                        return f"🤖 {personality_name} est connecté ! Prêt à être sarcastique... 😏"
                except AttributeError:
                    # Fallback si l'accès aux propriétés échoue
                    return f"🤖 {personality_name} est connecté ! Prêt à être sarcastique... 😏"
            else:
                return (
                    "🤖 nova_the_red_cat est connecté ! Prêt à être sarcastique... 😏"
                )

        except Exception as e:
            logger.error(f"Erreur lors de la génération du message de démarrage: {e}")
            return "🤖 nova_the_red_cat est connecté ! (avec quelques bugs...) 🤖"

    def stop(self):
        """Arrête le gestionnaire de chat"""
        try:
            self.is_active = False
            if self.message_processor:
                self.message_processor.stop_processing()
            logger.info("Gestionnaire de chat arrêté")

        except Exception as e:
            logger.error(f"Erreur lors de l'arrêt du gestionnaire de chat: {e}")

    async def send_manual_message(self, message: str):
        """
        Envoie un message manuellement

        Args:
            message: Message à envoyer
        """
        try:
            await self._send_message_callback(message)
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi manuel: {e}")

    async def trigger_manual_personality_change(self) -> str:
        """
        Déclenche manuellement un changement de personnalité

        Returns:
            str: Message d'annonce du changement
        """
        try:
            event_msg = await self.event_handler.handle_manual_change("manual_trigger")
            if event_msg:
                await self._send_message_callback(event_msg)
                return event_msg
            else:
                return "🤖 Changement de personnalité en cooldown !"

        except Exception as e:
            logger.error(f"Erreur lors du changement manuel: {e}")
            return "🤖 Erreur lors du changement de personnalité !"

    def get_status(self) -> dict:
        """
        Retourne le statut complet du gestionnaire de chat

        Returns:
            dict: Informations de statut
        """
        status = {
            "active": self.is_active,
            "initialized": self.message_processor is not None,
            "ai_handler_status": (
                self.ai_handler.get_status() if self.ai_handler else None
            ),
            "twitch_handler_status": (
                self.twitch_handler.get_connection_status()
                if self.twitch_handler
                else None
            ),
        }

        if self.message_processor:
            status["message_processor_status"] = self.message_processor.get_status()

        return status

    def test_response_generation(
        self, test_username: str = "testuser", test_message: str = "Hello bot!"
    ) -> bool:
        """
        Test la génération de réponse

        Args:
            test_username: Nom d'utilisateur de test
            test_message: Message de test

        Returns:
            bool: True si le test réussit
        """
        try:
            trigger_info = self.mention_detector.get_trigger_info(
                test_username, test_message
            )
            logger.info(f"Test de déclenchement: {trigger_info}")
            return True

        except Exception as e:
            logger.error(f"Erreur lors du test: {e}")
            return False
