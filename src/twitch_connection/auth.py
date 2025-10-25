"""
Module d'authentification pour Twitch
"""

import os
from dotenv import load_dotenv
from typing import Tuple, cast


class TwitchAuth:
    """Gère l'authentification Twitch"""

    def __init__(self):
        """Initialise l'authentification en chargeant les variables d'environnement"""
        load_dotenv()
        self.bot_token: str = ""
        self.client_id: str = ""
        self.channel_name: str = ""
        self.bot_name: str = ""
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Charge les identifiants depuis les variables d'environnement"""
        bot_token = os.getenv("TWITCH_BOT_TOKEN")
        client_id = os.getenv("TWITCH_BOT_CLIENT_ID")
        channel_name = os.getenv("TWITCH_CHANNEL")
        bot_name = os.getenv("TWITCH_BOT_NAME")

        if not all([bot_token, client_id, channel_name, bot_name]):
            raise ValueError("Identifiants Twitch manquants dans le fichier .env")

        self.bot_token = cast(str, bot_token)
        self.client_id = cast(str, client_id)
        self.channel_name = cast(str, channel_name)
        self.bot_name = cast(str, bot_name)

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
                len(self.bot_token) > 10,
                len(self.client_id) > 10,
                len(self.channel_name) > 0,
                len(self.bot_name) > 0,
            ]
        )
