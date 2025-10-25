"""
Module d'authentification pour Twitch
"""

import os
from dotenv import load_dotenv
from typing import Tuple


class TwitchAuth:
    """Gère l'authentification Twitch"""

    def __init__(self):
        """Initialise l'authentification en chargeant les variables d'environnement"""
        load_dotenv()
        self.bot_token = None
        self.client_id = None
        self.channel_name = None
        self.bot_name = None
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Charge les identifiants depuis les variables d'environnement"""
        self.bot_token = os.getenv("TWITCH_BOT_TOKEN")
        self.client_id = os.getenv("TWITCH_BOT_CLIENT_ID")
        self.channel_name = os.getenv("TWITCH_CHANNEL")
        self.bot_name = os.getenv("TWITCH_BOT_NAME")

        if not all([self.bot_token, self.client_id, self.channel_name, self.bot_name]):
            raise ValueError("Identifiants Twitch manquants dans le fichier .env")

    def get_credentials(self) -> Tuple[str, str, str, str]:
        """
        Retourne les identifiants Twitch

        Returns:
            Tuple[str, str, str, str]: token, client_id, channel_name, bot_name
        """
        return self.bot_token, self.client_id, self.channel_name, self.bot_name

    def validate_credentials(self) -> bool:
        """
        Valide que tous les identifiants sont présents

        Returns:
            bool: True si tous les identifiants sont valides
        """
        return all(
            [
                self.bot_token and len(self.bot_token) > 10,
                self.client_id and len(self.client_id) > 10,
                self.channel_name and len(self.channel_name) > 0,
                self.bot_name and len(self.bot_name) > 0,
            ]
        )
