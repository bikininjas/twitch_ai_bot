"""
Détecteur de mentions et conditions d'interaction
"""

import re
import logging
from typing import Tuple, List
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class MentionDetector:
    """Détecte les mentions du bot et détermine quand répondre"""

    def __init__(self):
        """Initialise le détecteur de mentions"""
        load_dotenv()
        self.bot_name = os.getenv("TWITCH_BOT_NAME", "").lower()
        self.owner_username = os.getenv("OWNER_USERNAME", "redpikpik").lower()

        # Patterns pour détecter les mentions
        self.mention_patterns = [
            rf"@{re.escape(self.bot_name)}",
            rf"\b{re.escape(self.bot_name)}\b",
            rf"{re.escape(self.bot_name)}[,!?]",
        ]

        logger.info(
            f"Détecteur initialisé - Bot: {self.bot_name}, Propriétaire: {self.owner_username}"
        )

    def should_respond(self, username: str, message: str) -> Tuple[bool, str]:
        """
        Détermine si le bot doit répondre au message

        Args:
            username: Nom de l'utilisateur
            message: Contenu du message

        Returns:
            Tuple[bool, str]: (doit_répondre, raison)
        """
        username_lower = username.lower()
        message_lower = message.lower()

        # Toujours répondre au propriétaire (redpikpik)
        if username_lower == self.owner_username:
            return True, "owner_message"

        # Vérifier les mentions directes du bot
        if self._is_bot_mentioned(message_lower):
            return True, "bot_mentioned"

        # Ne pas répondre aux autres cas
        return False, "no_trigger"

    def _is_bot_mentioned(self, message: str) -> bool:
        """
        Vérifie si le bot est mentionné dans le message

        Args:
            message: Message à analyser (en minuscules)

        Returns:
            bool: True si le bot est mentionné
        """
        for pattern in self.mention_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True
        return False

    def is_owner(self, username: str) -> bool:
        """
        Vérifie si l'utilisateur est le propriétaire du canal

        Args:
            username: Nom de l'utilisateur

        Returns:
            bool: True si c'est le propriétaire
        """
        return username.lower() == self.owner_username

    def extract_mentions(self, message: str) -> List[str]:
        """
        Extrait toutes les mentions d'utilisateurs du message

        Args:
            message: Message à analyser

        Returns:
            List[str]: Liste des utilisateurs mentionnés
        """
        mention_pattern = r"@(\w+)"
        mentions = re.findall(mention_pattern, message)
        return [mention.lower() for mention in mentions]

    def clean_message_for_ai(self, message: str) -> str:
        """
        Nettoie le message avant de l'envoyer à l'IA

        Args:
            message: Message original

        Returns:
            str: Message nettoyé
        """
        # Supprime les mentions du bot pour éviter la redondance
        cleaned = message
        for pattern in self.mention_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Nettoie les espaces multiples
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned

    def get_trigger_info(self, username: str, message: str) -> dict:
        """
        Retourne les informations détaillées sur le déclenchement

        Args:
            username: Nom de l'utilisateur
            message: Message à analyser

        Returns:
            dict: Informations de déclenchement
        """
        should_respond, reason = self.should_respond(username, message)

        return {
            "should_respond": should_respond,
            "trigger_reason": reason,
            "is_owner": self.is_owner(username),
            "is_mentioned": self._is_bot_mentioned(message.lower()),
            "mentions_found": self.extract_mentions(message),
            "cleaned_message": self.clean_message_for_ai(message),
        }
