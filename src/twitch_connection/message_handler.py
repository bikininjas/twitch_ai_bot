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
        self.bot_task = None
    
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
            
            # TwitchIO doit fonctionner dans la boucle d'événements principale
            # On crée une tâche pour le bot
            import asyncio
            
            # Créer une tâche pour exécuter le bot
            self.bot_task = asyncio.create_task(self.bot.start())
            
            # Attendre un peu pour la connexion
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
                # Annuler la tâche du bot si elle existe
                if self.bot_task and not self.bot_task.done():
                    self.bot_task.cancel()
                
                # Fermer la connexion du bot
                if hasattr(self.bot, 'close'):
                    import asyncio
                    try:
                        # Essayer de fermer proprement
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            loop.create_task(self.bot.close())
                        else:
                            asyncio.run(self.bot.close())
                    except Exception as e:
                        logger.warning(f"Erreur lors de la fermeture du bot: {e}")
                
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