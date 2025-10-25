"""
Configuration et authentification pour Google Gemini AI
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class GeminiConfig:
    """Configuration pour l'API Google Gemini"""

    def __init__(self):
        """Initialise la configuration Gemini"""
        load_dotenv()
        self.api_key = None
        self.model = None
        self._load_config()

    def _load_config(self):
        """Charge la configuration depuis les variables d'environnement"""
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("Clé API Gemini manquante dans le fichier .env")

        # Configuration de l'API
        genai.configure(api_key=self.api_key)

        # Initialisation du modèle
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        logger.info("Configuration Gemini initialisée avec succès")

    def get_model(self):
        """
        Retourne le modèle Gemini configuré

        Returns:
            GenerativeModel: Modèle Gemini prêt à utiliser
        """
        if not self.model:
            raise RuntimeError("Modèle Gemini non initialisé")
        return self.model

    def test_connection(self) -> bool:
        """
        Test la connexion à l'API Gemini

        Returns:
            bool: True si la connexion fonctionne
        """
        try:
            # Test simple avec une requête basique
            response = self.model.generate_content("Dis bonjour")
            return bool(response.text)
        except Exception as e:
            logger.error(f"Erreur lors du test de connexion Gemini: {e}")
            return False
