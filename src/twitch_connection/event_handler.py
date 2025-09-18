"""
Gestionnaire d'événements Twitch pour déclencher les changements de personnalité
"""

import logging
import asyncio
from typing import Callable, Optional
from twitchio.ext import commands
from twitchio import Message

logger = logging.getLogger(__name__)

class TwitchEventHandler:
    """Gestionnaire des événements Twitch (follow, sub, gift, etc.)"""
    
    def __init__(self, personality_change_callback: Callable[[str], None]):
        """
        Initialise le gestionnaire d'événements
        
        Args:
            personality_change_callback: Function appelée pour changer de personnalité
        """
        self.personality_change_callback = personality_change_callback
        self.event_cooldown = {}  # Cooldown pour éviter le spam
        self.cooldown_time = 300  # 5 minutes entre changements pour le même type d'événement
        
        logger.info("Gestionnaire d'événements Twitch initialisé")
    
    async def handle_subscription(self, subscriber_name: str, tier: str = "1000", months: int = 1):
        """
        Gère un nouvel abonnement
        
        Args:
            subscriber_name: Nom du nouvel abonné
            tier: Tier de l'abonnement (1000, 2000, 3000)
            months: Nombre de mois
        """
        try:
            event_type = "subscription"
            
            if not self._is_event_on_cooldown(event_type):
                logger.info(f"Nouvel abonnement détecté: {subscriber_name} (Tier {tier}, {months} mois)")
                
                # Message d'événement avec changement de personnalité
                event_message = await self._trigger_personality_change(
                    event_type=event_type,
                    trigger_user=subscriber_name,
                    event_details=f"vient de s'abonner (Tier {tier}) ! 🎉"
                )
                
                return event_message
            else:
                logger.debug(f"Abonnement ignoré (cooldown): {subscriber_name}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la gestion de l'abonnement: {e}")
            return None
    
    async def handle_follow(self, follower_name: str):
        """
        Gère un nouveau follow
        
        Args:
            follower_name: Nom du nouveau follower
        """
        try:
            event_type = "follow"
            
            if not self._is_event_on_cooldown(event_type):
                logger.info(f"Nouveau follow détecté: {follower_name}")
                
                # Message d'événement avec changement de personnalité
                event_message = await self._trigger_personality_change(
                    event_type=event_type,
                    trigger_user=follower_name,
                    event_details="vient de follow ! 💜"
                )
                
                return event_message
            else:
                logger.debug(f"Follow ignoré (cooldown): {follower_name}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la gestion du follow: {e}")
            return None
    
    async def handle_gift_subscription(self, gifter_name: str, recipient_name: str, tier: str = "1000"):
        """
        Gère un gift sub
        
        Args:
            gifter_name: Nom de la personne qui offre
            recipient_name: Nom du bénéficiaire
            tier: Tier de l'abonnement
        """
        try:
            event_type = "gift_sub"
            
            if not self._is_event_on_cooldown(event_type):
                logger.info(f"Gift sub détecté: {gifter_name} -> {recipient_name} (Tier {tier})")
                
                # Message d'événement avec changement de personnalité
                event_message = await self._trigger_personality_change(
                    event_type=event_type,
                    trigger_user=gifter_name,
                    event_details=f"offre un sub à {recipient_name} ! Généreux ! 🎁"
                )
                
                return event_message
            else:
                logger.debug(f"Gift sub ignoré (cooldown): {gifter_name}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la gestion du gift sub: {e}")
            return None
    
    async def handle_cheer(self, cheerer_name: str, bits: int):
        """
        Gère un cheer (bits)
        
        Args:
            cheerer_name: Nom de la personne qui cheer
            bits: Nombre de bits
        """
        try:
            # Seulement pour les gros cheers (100+ bits)
            if bits < 100:
                return None
            
            event_type = "cheer"
            
            if not self._is_event_on_cooldown(event_type):
                logger.info(f"Gros cheer détecté: {cheerer_name} ({bits} bits)")
                
                # Message d'événement avec changement de personnalité
                event_message = await self._trigger_personality_change(
                    event_type=event_type,
                    trigger_user=cheerer_name,
                    event_details=f"balance {bits} bits ! Ca fait du bruit ! 💰"
                )
                
                return event_message
            else:
                logger.debug(f"Cheer ignoré (cooldown): {cheerer_name}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la gestion du cheer: {e}")
            return None
    
    async def handle_raid(self, raider_name: str, viewer_count: int):
        """
        Gère un raid
        
        Args:
            raider_name: Nom du raideur
            viewer_count: Nombre de viewers dans le raid
        """
        try:
            event_type = "raid"
            
            if not self._is_event_on_cooldown(event_type):
                logger.info(f"Raid détecté: {raider_name} avec {viewer_count} viewers")
                
                # Message d'événement avec changement de personnalité
                event_message = await self._trigger_personality_change(
                    event_type=event_type,
                    trigger_user=raider_name,
                    event_details=f"nous raid avec {viewer_count} viewers ! INVASION ! 🏴‍☠️"
                )
                
                return event_message
            else:
                logger.debug(f"Raid ignoré (cooldown): {raider_name}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la gestion du raid: {e}")
            return None
    
    async def handle_manual_change(self, trigger_user: str = "manuel"):
        """
        Gère un changement manuel de personnalité (pour tests)
        
        Args:
            trigger_user: Nom de l'utilisateur ou "manuel"
            
        Returns:
            str: Message d'annonce ou None si en cooldown
        """
        try:
            event_type = "manual"
            
            if not self._is_event_on_cooldown(event_type):
                logger.info(f"Changement manuel de personnalité déclenché par: {trigger_user}")
                
                # Message d'événement avec changement de personnalité
                event_message = await self._trigger_personality_change(
                    event_type=event_type,
                    trigger_user=trigger_user,
                    event_details="a déclenché un changement de personnalité ! 🎲"
                )
                
                return event_message
            else:
                logger.debug(f"Changement manuel ignoré (cooldown): {trigger_user}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors du changement manuel: {e}")
            return None
    
    async def _trigger_personality_change(self, event_type: str, trigger_user: str, event_details: str) -> str:
        """
        Déclenche un changement de personnalité et génère le message d'annonce
        
        Args:
            event_type: Type d'événement
            trigger_user: Utilisateur qui a déclenché l'événement
            event_details: Détails de l'événement
            
        Returns:
            str: Message d'annonce combiné
        """
        try:
            # Déclencher le changement de personnalité (forcer pour les vrais événements)
            force_change = event_type != "manual"  # Forcer sauf pour les changements manuels
            personality_announcement = await self.personality_change_callback(event_type, force_change)
            
            if personality_announcement is None:
                # En cooldown, juste annoncer l'événement
                logger.debug(f"Changement de personnalité ignoré (cooldown) pour {event_type}")
                return f"🎊 {trigger_user} {event_details}"
            
            # Créer le message complet
            event_msg = f"🎊 {trigger_user} {event_details}"
            full_message = f"{event_msg} \\n{personality_announcement}"
            
            # Marquer le cooldown
            self._set_event_cooldown(event_type)
            
            logger.info(f"Changement de personnalité déclenché par {event_type}: {trigger_user}")
            
            return full_message
            
        except Exception as e:
            logger.error(f"Erreur lors du changement de personnalité: {e}")
            return f"🎊 {trigger_user} {event_details}"
    
    def _is_event_on_cooldown(self, event_type: str) -> bool:
        """
        Vérifie si un type d'événement est en cooldown
        
        Args:
            event_type: Type d'événement à vérifier
            
        Returns:
            bool: True si en cooldown
        """
        import time
        
        if event_type not in self.event_cooldown:
            return False
        
        return time.time() - self.event_cooldown[event_type] < self.cooldown_time
    
    def _set_event_cooldown(self, event_type: str):
        """
        Démarre le cooldown pour un type d'événement
        
        Args:
            event_type: Type d'événement
        """
        import time
        self.event_cooldown[event_type] = time.time()
    
    def get_cooldown_status(self) -> dict:
        """
        Retourne le statut des cooldowns
        
        Returns:
            dict: Statut des cooldowns par type d'événement
        """
        import time
        current_time = time.time()
        
        status = {}
        for event_type, cooldown_start in self.event_cooldown.items():
            remaining = max(0, self.cooldown_time - (current_time - cooldown_start))
            status[event_type] = {
                "on_cooldown": remaining > 0,
                "remaining_seconds": int(remaining)
            }
        
        return status


class TwitchEventListener:
    """Listener pour intégrer les événements TwitchIO avec le gestionnaire d'événements"""
    
    def __init__(self, event_handler: TwitchEventHandler, message_sender: Callable[[str], None]):
        """
        Initialise le listener d'événements
        
        Args:
            event_handler: Gestionnaire d'événements
            message_sender: Function pour envoyer des messages
        """
        self.event_handler = event_handler
        self.message_sender = message_sender
        
        logger.info("Listener d'événements Twitch initialisé")
    
    async def on_message(self, message: Message):
        """
        Analyse les messages pour détecter des événements (fallback)
        
        Args:
            message: Message Twitch reçu
        """
        try:
            # Détecter des patterns dans les messages du bot Twitch officiel
            content = message.content.lower()
            author = message.author.name.lower()
            
            # Messages de follow (détection par pattern)
            if "followed" in content or "following" in content:
                # Essayer d'extraire le nom du follower
                if message.author.name != "redpikpik":  # Pas nous-mêmes
                    event_msg = await self.event_handler.handle_follow(message.author.name)
                    if event_msg:
                        await self.message_sender(event_msg)
            
            # Messages de sub (détection par pattern)
            elif "subscribed" in content or "subscriber" in content:
                event_msg = await self.event_handler.handle_subscription(
                    message.author.name, 
                    tier="1000"  # Par défaut
                )
                if event_msg:
                    await self.message_sender(event_msg)
            
            # Messages de bits (détection par pattern)
            elif "cheer" in content or "bits" in content:
                # Essayer d'extraire le nombre de bits
                import re
                bits_match = re.search(r'cheer(\d+)', content)
                if bits_match:
                    bits = int(bits_match.group(1))
                    event_msg = await self.event_handler.handle_cheer(message.author.name, bits)
                    if event_msg:
                        await self.message_sender(event_msg)
                        
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du message pour événements: {e}")
    
    async def on_follow(self, follower):
        """
        Handler direct pour les follows (si supporté par TwitchIO)
        
        Args:
            follower: Objet follower
        """
        try:
            event_msg = await self.event_handler.handle_follow(follower.name)
            if event_msg:
                await self.message_sender(event_msg)
        except Exception as e:
            logger.error(f"Erreur lors de la gestion du follow direct: {e}")
    
    async def on_subscription(self, subscription):
        """
        Handler direct pour les subs (si supporté par TwitchIO)
        
        Args:
            subscription: Objet subscription
        """
        try:
            event_msg = await self.event_handler.handle_subscription(
                subscription.user.name,
                subscription.tier if hasattr(subscription, 'tier') else "1000",
                subscription.cumulative_months if hasattr(subscription, 'cumulative_months') else 1
            )
            if event_msg:
                await self.message_sender(event_msg)
        except Exception as e:
            logger.error(f"Erreur lors de la gestion du sub direct: {e}")