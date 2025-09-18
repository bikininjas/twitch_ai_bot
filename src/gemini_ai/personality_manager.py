"""
Gestionnaire de personnalités multiples pour nova_the_red_cat
"""

import logging
import random
import time
from typing import Dict, List, Tuple, Optional

from .personalities import Personality, PersonalityType, create_all_personalities

logger = logging.getLogger(__name__)

class PersonalityManager:
    """Gestionnaire des personnalités multiples du bot"""
    
    def __init__(self, cooldown_time: int = 300):  # 5 minutes de cooldown par défaut
        self.personalities: Dict[PersonalityType, Personality] = create_all_personalities()
        self.current_personality: Optional[Personality] = None
        self.cooldown_time = cooldown_time
        self.last_change_time = 0.0
        self.personality_history: List[PersonalityType] = []
        
        # Sélectionner une personnalité aléatoire au démarrage
        self.change_personality(force=True)
    
    def get_random_personality(self, exclude_current: bool = True) -> Personality:
        """Sélectionne une personnalité aléatoire"""
        available = list(self.personalities.values())
        if exclude_current and self.current_personality:
            available = [p for p in available if p.type != self.current_personality.type]
        return random.choice(available)
    
    def change_personality(self, new_personality: Optional[PersonalityType] = None, force: bool = False) -> Tuple[bool, str]:
        """Change la personnalité du bot avec système de cooldown"""
        current_time = time.time()
        
        # Vérifier le cooldown (sauf si forcé)
        if not force and (current_time - self.last_change_time) < self.cooldown_time:
            remaining = int(self.cooldown_time - (current_time - self.last_change_time))
            return False, f"⏰ Changement de personnalité en cooldown ! Encore {remaining} secondes..."
        
        # Sélectionner la nouvelle personnalité
        if new_personality and new_personality in self.personalities:
            personality = self.personalities[new_personality]
        else:
            personality = self.get_random_personality()
        
        # Éviter les doublons (sauf si forcé)
        if not force and self.current_personality and personality.type == self.current_personality.type:
            personality = self.get_random_personality()
        
        # Appliquer le changement
        old_personality = self.current_personality.name if self.current_personality else "aucune"
        self.current_personality = personality
        self.last_change_time = current_time
        self.personality_history.append(personality.type)
        
        # Garder seulement les 10 dernières personnalités dans l'historique
        if len(self.personality_history) > 10:
            self.personality_history = self.personality_history[-10:]
        
        # Choisir une annonce aléatoire
        announcement = random.choice(personality.announcement_variants)
        
        logger.info(f"Changement de personnalité : {old_personality} -> {personality.name}")
        
        return True, announcement
    
    def get_current_prompt(self) -> str:
        """Retourne le prompt de la personnalité actuelle"""
        if not self.current_personality:
            self.change_personality(force=True)
        return self.current_personality.prompt_base
    
    def get_personality_signature(self) -> str:
        """Retourne la signature de la personnalité actuelle"""
        if not self.current_personality:
            self.change_personality(force=True)
        return self.current_personality.signature
    
    def get_current_personality_name(self) -> str:
        """Retourne le nom de la personnalité actuelle"""
        if not self.current_personality:
            self.change_personality(force=True)
        return self.current_personality.name
    
    def get_startup_message(self) -> str:
        """Génère un message de démarrage avec la personnalité actuelle"""
        if not self.current_personality:
            self.change_personality(force=True)
        
        # Choisir une variante d'annonce aléatoire pour le démarrage
        announcement = random.choice(self.current_personality.announcement_variants)
        
        return f"🤖 {self.current_personality.name} est connecté ! {announcement}"
    
    def get_personality_stats(self) -> Dict:
        """Retourne les statistiques des personnalités"""
        return {
            "current": self.current_personality.name if self.current_personality else None,
            "available_count": len(self.personalities),
            "history": [p.value for p in self.personality_history[-5:]],  # 5 dernières
            "all_personalities": [p.name for p in self.personalities.values()]
        }
    
    def get_random_catchphrase(self) -> str:
        """Retourne une phrase d'accroche aléatoire de la personnalité actuelle"""
        if not self.current_personality:
            self.change_personality(force=True)
        return random.choice(self.current_personality.catchphrases)
    
    def force_personality(self, personality_type: PersonalityType) -> Tuple[bool, str]:
        """Force une personnalité spécifique (bypass du cooldown)"""
        return self.change_personality(personality_type, force=True)
    
    def get_cooldown_remaining(self) -> int:
        """Retourne le temps de cooldown restant en secondes"""
        current_time = time.time()
        remaining = max(0, int(self.cooldown_time - (current_time - self.last_change_time)))
        return remaining
    
    def list_available_personalities(self) -> List[str]:
        """Retourne la liste des personnalités disponibles"""
        return [f"{p.type.value} ({p.name})" for p in self.personalities.values()]