"""
Module de connexion IRC pour Twitch
"""

import asyncio
import logging
from twitchio.ext import commands
from typing import Callable, Optional
from .auth import TwitchAuth

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


class TwitchBot(commands.Bot):
    """Bot Twitch utilisant l'IRC"""

    def __init__(self, message_callback: Callable[[str, str], None] = None):
        """
        Initialise le bot Twitch

        Args:
            message_callback: Fonction appelée lors de la réception d'un message
        """
        self.auth = TwitchAuth()
        token, client_id, channel, bot_name = self.auth.get_credentials()

        # Initialisation du bot TwitchIO
        super().__init__(
            token=token,
            client_id=client_id,
            nick=bot_name,
            prefix="!",
            initial_channels=[channel],
        )

        # Sauvegarder les informations pour debug
        self.target_channel = channel
        self.message_callback = message_callback
        self._stored_token = token
        self._stored_client_id = client_id

        logger.info(f"Bot initialisé pour le canal: {channel}")
        logger.debug(f"Token: {token[:10]}... | Client ID: {client_id[:10]}...")

    async def event_ready(self):
        """Événement déclenché quand le bot est connecté"""
        logger.info(f'🎉 Bot "nova_the_red_cat" connecté (compte: {self.nick})')
        logger.info(f"🆔 ID utilisateur: {self.user_id}")
        logger.debug(
            f"📺 Canaux rejoints: {[channel.name for channel in self.connected_channels]}"
        )
        logger.debug(f"🔑 Token utilisé: {self._stored_token[:10]}...")
        logger.debug(f"🆔 Client ID: {self._stored_client_id[:10]}...")

        # Envoyer un message de test de connexion
        await self.send_connection_test_message()

    async def send_connection_test_message(self):
        """Envoie un message de test pour confirmer que le bot peut écrire"""
        try:
            await asyncio.sleep(2)  # Attendre un peu après la connexion
            test_message = "🤖 Nova est de retour ! Prêt à être sarcastique... 😏"
            await self.send_message(test_message)
            logger.info("✅ Message de test envoyé avec succès")
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'envoi du message de test: {e}")

    async def event_message(self, message):
        """
        Événement déclenché à chaque message reçu

        Args:
            message: Message reçu de Twitch
        """
        # Ignorer nos propres messages
        if message.echo:
            logger.debug("Message ignoré (echo du bot)")
            return

        logger.info(f"Message de {message.author.name}: {message.content}")
        logger.debug(f"Canal: {message.channel.name}, Tags: {message.tags}")

        # Appeler le callback si défini
        if self.message_callback:
            await asyncio.create_task(
                self._handle_message_async(message.author.name, message.content)
            )

    async def _handle_message_async(self, username: str, content: str):
        """
        Gère les messages de façon asynchrone

        Args:
            username: Nom de l'utilisateur
            content: Contenu du message
        """
        try:
            if asyncio.iscoroutinefunction(self.message_callback):
                await self.message_callback(username, content)
            else:
                self.message_callback(username, content)
        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")

    async def send_message(self, content: str, channel: Optional[str] = None):
        """
        Envoie un message dans le chat

        Args:
            content: Contenu du message à envoyer
            channel: Canal où envoyer (par défaut le canal configuré)
        """
        target = channel or self.target_channel
        try:
            channel_obj = self.get_channel(target)
            if channel_obj:
                await channel_obj.send(content)
                logger.info(f"Message envoyé dans {target}: {content}")
            else:
                logger.error(f"Canal {target} non trouvé")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message: {e}")

    async def start_bot(self):
        """Démarre le bot de façon asynchrone"""
        try:
            await self.start()
        except Exception as e:
            logger.error(f"Erreur lors du démarrage du bot: {e}")
            raise
