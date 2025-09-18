"""
Générateur de réponses avec personnalités multiples et Gemini
"""

import logging
import random
from typing import Optional
from .config import GeminiConfig
from .personality_manager import PersonalityManager

logger = logging.getLogger(__name__)

class GeminiResponseGenerator:
    """Génère des réponses personnalisées avec Gemini AI et personnalités multiples"""
    
    def __init__(self):
        """Initialise le générateur de réponses"""
        self.config = GeminiConfig()
        self.model = self.config.get_model()
        self.personality_manager = PersonalityManager()
        
        # Initialiser avec une personnalité aléatoire (force le premier changement)
        self.personality_manager.change_personality(force=True)
        
        # Phrases d'accroche dynamiques selon la personnalité
        self.dynamic_starters = [
            "Oh regarde qui parle... ",
            "Alors {username}, ",
            "Eh bien {username}, ",
            "Tiens tiens, {username} ",
            "Ah {username}, toujours aussi... ",
        ]
    
    async def generate_response(self, username: str, message: str, is_owner: bool = False) -> str:
        """
        Génère une réponse personnalisée selon la personnalité actuelle
        
        Args:
            username: Nom de l'utilisateur
            message: Message original
            is_owner: True si c'est le propriétaire du canal
            
        Returns:
            str: Réponse générée par Gemini
        """
        try:
            # Construction du prompt avec la personnalité actuelle
            prompt = self._build_prompt(username, message, is_owner)
            
            # Génération avec Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                # Nettoyage et validation de la réponse
                clean_response = self._clean_response(response.text, username)
                logger.info(f"Réponse générée pour {username}: {clean_response}")
                return clean_response
            else:
                return self._get_fallback_response(username)
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse: {e}")
            return self._get_fallback_response(username)
    
    def _build_prompt(self, username: str, message: str, is_owner: bool) -> str:
        """
        Construit le prompt pour Gemini avec la personnalité actuelle
        
        Args:
            username: Nom de l'utilisateur
            message: Message original
            is_owner: True si c'est le propriétaire
            
        Returns:
            str: Prompt formaté
        """
        owner_instruction = ""
        if is_owner:
            owner_instruction = "L'utilisateur est le propriétaire du canal, sois un peu plus respectueux mais garde ta personnalité."
        
        # Utiliser une phrase d'accroche de la personnalité actuelle
        catchphrase = self.personality_manager.get_random_catchphrase()
        starter = f"{catchphrase} {username}, "
        
        # Obtenir le prompt de base de la personnalité actuelle
        personality_prompt = self.personality_manager.get_personality_prompt()
        
        prompt = f"""
        {personality_prompt}
        
        {owner_instruction}
        
        L'utilisateur '{username}' a dit: "{message}"
        
        Génère une réponse qui commence par: "{starter}"
        
        Essaie de faire un jeu de mots avec le pseudo '{username}' si possible.
        
        Réponse (max 200 caractères):
        """
        
        return prompt
    
    def _clean_response(self, response: str, username: str) -> str:
        """
        Nettoie et valide la réponse de Gemini avec signature de personnalité
        
        Args:
            response: Réponse brute de Gemini
            username: Nom de l'utilisateur pour validation
            
        Returns:
            str: Réponse nettoyée avec signature
        """
        # Suppression des guillemets et caractères indésirables
        cleaned = response.strip().strip('"').strip("'")
        
        # Obtenir la signature de la personnalité actuelle
        signature = self.personality_manager.get_personality_signature()
        
        # Ajouter la signature si elle n'est pas déjà présente
        if not any(sig in cleaned for sig in ["- nova", "nova 🐱", "nova ⚡", "nova 🌙", "nova 🧠", "nova 😡", "nova 😴", "nova 🎭", "nova 💕"]):
            cleaned = f"{cleaned} {signature}"
        
        # Limitation de la longueur
        if len(cleaned) > 200:
            cleaned = cleaned[:197] + "..."
        
        # Vérification que le username est mentionné
        if username.lower() not in cleaned.lower():
            cleaned = f"@{username} {cleaned}"
        
        return cleaned
    
    def _get_fallback_response(self, username: str) -> str:
        """
        Génère une réponse de secours en cas d'erreur selon la personnalité
        
        Args:
            username: Nom de l'utilisateur
            
        Returns:
            str: Réponse de secours avec personnalité
        """
        signature = self.personality_manager.get_personality_signature()
        
        fallbacks = [
            f"@{username} Mon cerveau a buggé... comme ton pseudo ! 🤖 {signature}",
            f"@{username} Je cherche encore une réponse... comme toi tu cherches le skill ! 😏 {signature}",
            f"@{username} Erreur 404: Esprit pas trouvé... mais toi non plus ! 💀 {signature}",
            f"@{username} Mon IA a crashé, mais pas autant que ton gameplay ! 🎮 {signature}",
        ]
        
        return random.choice(fallbacks)
    
    def change_personality(self, new_personality=None, force: bool = False):
        """
        Change la personnalité du bot et retourne le message d'annonce
        
        Args:
            new_personality: Personnalité spécifique ou None pour aléatoire
            force: Ignorer le cooldown
            
        Returns:
            str: Message d'annonce du changement
            
        Raises:
            ValueError: Si en cooldown et force=False
        """
        personality, announcement = self.personality_manager.change_personality(new_personality, force)
        logger.info(f"Personnalité changée vers: {personality.name}")
        return announcement
    
    def get_current_personality_name(self) -> str:
        """Retourne le nom de la personnalité actuelle"""
        current = self.personality_manager.get_current_personality()
        return current.name if current else "nova_the_red_cat"
    
    def get_personality_stats(self) -> dict:
        """Retourne les statistiques des personnalités"""
        return self.personality_manager.get_personality_stats()
    
    def generate_pun_with_username(self, username: str) -> Optional[str]:
        """
        Génère un jeu de mots spécifique avec le nom d'utilisateur
        
        Args:
            username: Nom de l'utilisateur
            
        Returns:
            str: Jeu de mots ou None si pas possible
        """
        try:
            prompt = f"""
            Crée un jeu de mots sarcastique et humoristique avec le pseudo Twitch '{username}'.
            Utilise des références gaming, internet ou populaires.
            Reste poli mais moqueur.
            Maximum 100 caractères.
            """
            
            response = self.model.generate_content(prompt)
            if response.text:
                return response.text.strip()
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de jeu de mots: {e}")
        
        return None