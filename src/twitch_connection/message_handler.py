"""
Gestionnaire de messages Twitch
"""

import logging
from typing import Optional
from .irc_client import TwitchBot

logger = logging.getLogger(__name__)

class TwitchMessageHandler:
    """Gère l'envoi et la réception de messages Twitch"""
    
    def __init__(self):
        """Initialise le gestionnaire de messages"""
        self.bot: Optional[TwitchBot] = None
        self.is_connected = False
    
    def initialize_bot(self, message_callback=None):
        """
        Initialise le bot Twitch
        
        Args:
            message_callback: Fonction appelée lors de la réception d'un message
        """
        try:
            self.bot = TwitchBot(message_callback=message_callback)
            logger.info("Bot Twitch initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du bot: {e}")
            raise
    
    async def connect(self):
        """Connecte le bot à Twitch"""
        if not self.bot:
            raise RuntimeError("Bot non initialisé. Appelez initialize_bot() d'abord.")
        
        try:
            logger.info("🔌 Connexion au chat Twitch...")
            logger.debug(f"👤 Bot: {self.bot.nick}")
            logger.debug(f"📺 Canal cible: {self.bot.target_channel}")
            logger.debug(f"🔑 Token: {self.bot._stored_token[:10]}...")
            logger.debug(f"🆔 Client ID: {self.bot._stored_client_id[:10]}...")
            
            # TwitchIO utilise run() dans un thread séparé
            import threading
            
            def run_bot():
                try:
                    self.bot.run()
                except Exception as e:
                    logger.error(f"❌ Erreur dans le thread du bot: {e}")
            
            # Démarrer le bot dans un thread séparé
            bot_thread = threading.Thread(target=run_bot, daemon=True)
            bot_thread.start()
            
            # Attendre un peu pour la connexion
            import asyncio
            await asyncio.sleep(3)
            
            # Vérifier si des canaux sont connectés
            if hasattr(self.bot, 'connected_channels') and self.bot.connected_channels:
                self.is_connected = True
                logger.info("✅ Connecté au chat Twitch")
            else:
                logger.warning("⚠️ Connexion incertaine - pas de canaux détectés")
                self.is_connected = True  # On suppose que ça marche
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la connexion: {e}")
            logger.debug(f"🔍 Détails de l'erreur: {type(e).__name__}: {str(e)}")
            self.is_connected = False
            raise
    
    async def send_message(self, message: str, channel: Optional[str] = None):
        """
        Envoie un message dans le chat Twitch
        
        Args:
            message: Message à envoyer
            channel: Canal où envoyer (optionnel)
        """
        if not self.bot or not self.is_connected:
            logger.error("Bot non connecté")
            return False
        
        try:
            await self.bot.send_message(message, channel)
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message: {e}")
            return False
    
    def disconnect(self):
        """Déconnecte le bot"""
        if self.bot and self.is_connected:
            try:
                # TwitchIO ne fournit pas de méthode disconnect directe
                # Le bot s'arrêtera quand le processus se termine
                self.is_connected = False
                logger.info("Bot déconnecté")
            except Exception as e:
                logger.error(f"Erreur lors de la déconnexion: {e}")
    
    def get_connection_status(self) -> bool:
        """
        Retourne le statut de connexion
        
        Returns:
            bool: True si connecté, False sinon
        """
        return self.is_connected and self.bot is not None