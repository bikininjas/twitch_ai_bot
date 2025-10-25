"""
Gestionnaire principal pour l'intégration Gemini AI
"""

import logging
import asyncio
from typing import Optional, List, Dict, Any
from .config import GeminiConfig
from .response_generator import GeminiResponseGenerator

logger = logging.getLogger(__name__)


class GeminiHandler:
    """Gestionnaire principal pour toutes les interactions avec Gemini AI"""

    def __init__(self):
        """Initialise le gestionnaire Gemini"""
        self.config = None
        self.response_generator = None
        self.is_initialized = False

    def initialize(self) -> bool:
        """
        Initialise les composants Gemini

        Returns:
            bool: True si l'initialisation réussit
        """
        try:
            self.config = GeminiConfig()
            self.response_generator = GeminiResponseGenerator()
            self.is_initialized = True
            logger.info("Gestionnaire Gemini initialisé avec succès")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation Gemini: {e}")
            self.is_initialized = False
            return False

    async def process_message(
        self, username: str, message: str, is_owner: bool = False
    ) -> Optional[str]:
        """
        Traite un message et génère une réponse

        Args:
            username: Nom de l'utilisateur
            message: Message à traiter
            is_owner: True si c'est le propriétaire du canal

        Returns:
            str: Réponse générée ou None si erreur
        """
        if not self.is_initialized or not self.response_generator:
            logger.error("Gestionnaire Gemini non initialisé")
            return None

        try:
            # Génération asynchrone de la réponse
            response = await self.response_generator.generate_response(
                username=username, message=message, is_owner=is_owner
            )

            return response

        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")
            return f"@{username} Mon cerveau a planté... Comme ton PC probablement ! 💥"

    def test_connection(self) -> bool:
        """
        Test la connexion à Gemini

        Returns:
            bool: True si la connexion fonctionne
        """
        if not self.is_initialized or not self.config:
            return False

        return self.config.test_connection()

    async def generate_pun(self, username: str) -> Optional[str]:
        """
        Génère un jeu de mots avec le nom d'utilisateur

        Args:
            username: Nom de l'utilisateur

        Returns:
            str: Jeu de mots généré ou None
        """
        if not self.is_initialized or not self.response_generator:
            return None

        try:
            return self.response_generator.generate_pun_with_username(username)
        except Exception as e:
            logger.error(f"Erreur lors de la génération de jeu de mots: {e}")
            return None

    def change_personality(
        self, new_personality=None, force: bool = False
    ) -> Optional[str]:
        """
        Change la personnalité du bot

        Args:
            new_personality: Personnalité spécifique ou None pour aléatoire
            force: Ignorer le cooldown

        Returns:
            str: Message d'annonce du changement
        """
        if not self.is_initialized or not self.response_generator:
            return "❌ Bot non initialisé"

        try:
            return self.response_generator.change_personality(new_personality, force)
        except ValueError as e:
            # Erreur de cooldown
            logger.debug(f"Changement de personnalité bloqué: {e}")
            return None
        except Exception as e:
            logger.error(f"Erreur lors du changement de personnalité: {e}")
            return "🤖 Quelque chose a foiré dans ma tête... Je reste comme je suis !"

    def get_current_personality_name(self) -> str:
        """Retourne le nom de la personnalité actuelle"""
        if not self.is_initialized or not self.response_generator:
            return "nova_the_unknown_cat"

        try:
            return self.response_generator.get_current_personality_name()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du nom de personnalité: {e}")
            return "nova_the_confused_cat"

    def get_personality_stats(self) -> dict:
        """Retourne les statistiques des personnalités"""
        if not self.is_initialized or not self.response_generator:
            return {}

        try:
            return self.response_generator.get_personality_stats()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return {}

    def list_personalities(self) -> List[Dict[str, Any]]:
        if not self.is_initialized or not self.response_generator:
            return []
        try:
            return self.response_generator.list_personalities()
        except Exception as e:
            logger.error(f"Erreur lors de la liste des personnalités: {e}")
            return []

    def get_personality_preview(self, identifier: str) -> Optional[Dict[str, object]]:
        if not self.is_initialized or not self.response_generator:
            return None
        try:
            return self.response_generator.get_personality_preview(identifier)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'aperçu: {e}")
            return None

    def get_current_triggers(self) -> Dict[str, List[str]]:
        if not self.is_initialized or not self.response_generator:
            return {"keywords": [], "commands": []}
        try:
            return self.response_generator.get_current_triggers()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des triggers: {e}")
            return {"keywords": [], "commands": []}

    def get_status(self) -> dict:
        """
        Retourne le statut du gestionnaire Gemini

        Returns:
            dict: Informations de statut
        """
        status: Dict[str, Any] = {
            "initialized": self.is_initialized,
            "config_loaded": self.config is not None,
            "generator_ready": self.response_generator is not None,
            "connection_ok": self.test_connection() if self.is_initialized else False,
        }

        # Ajouter les informations de personnalité
        if self.is_initialized:
            status["personality"] = {
                "current": self.get_current_personality_name(),
                "stats": self.get_personality_stats(),
            }

        return status
