"""
Processeur de messages pour le chat Twitch
"""

import logging
import asyncio
from typing import Optional, Callable
from .mention_detector import MentionDetector

logger = logging.getLogger(__name__)


class MessageProcessor:
    """Traite les messages entrants et détermine les actions à prendre"""

    def __init__(self, ai_handler, response_callback: Optional[Callable] = None):
        """
        Initialise le processeur de messages

        Args:
            ai_handler: Instance du gestionnaire IA (Gemini)
            response_callback: Fonction pour envoyer les réponses
        """
        self.ai_handler = ai_handler
        self.response_callback = response_callback
        self.mention_detector = MentionDetector()
        self.message_queue = asyncio.Queue()
        self.processing = False

        logger.info("Processeur de messages initialisé")

    async def process_message(self, username: str, message: str) -> bool:
        """
        Traite un message entrant

        Args:
            username: Nom de l'utilisateur
            message: Contenu du message

        Returns:
            bool: True si le message a été traité et une réponse générée
        """
        try:
            # Vérifier d'abord les commandes spéciales
            if await self._handle_special_commands(username, message):
                return True

            # Analyser le déclenchement normal
            trigger_info = self.mention_detector.get_trigger_info(username, message)

            # Détection des triggers personnalisés
            extra_trigger = self._check_personality_triggers(message)
            if extra_trigger:
                trigger_info["should_respond"] = True
                trigger_info["trigger_reason"] = extra_trigger

            logger.info(f"Message de {username}: {message}")
            logger.info(f"Trigger info: {trigger_info}")

            # Vérifier si on doit répondre
            if not trigger_info["should_respond"]:
                logger.debug(
                    f"Pas de réponse nécessaire: {trigger_info['trigger_reason']}"
                )
                return False

            # Générer la réponse avec l'IA
            response = await self._generate_ai_response(
                username=username,
                message=trigger_info["cleaned_message"],
                is_owner=trigger_info["is_owner"],
                trigger_reason=trigger_info["trigger_reason"],
            )

            if response:
                # Envoyer la réponse
                await self._send_response(response)
                return True

            return False

        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")
            return False

    async def _handle_special_commands(self, username: str, message: str) -> bool:
        """
        Gère les commandes spéciales (changement de personnalité, etc.)

        Args:
            username: Nom de l'utilisateur
            message: Contenu du message

        Returns:
            bool: True si une commande spéciale a été traitée
        """
        try:
            message_lower = message.lower().strip()

            # Commandes accessibles à tous concernant les personnalités
            if await self._handle_persona_commands(username, message, message_lower):
                return True

            # Commandes disponibles seulement pour le propriétaire
            is_owner = username.lower() == "redpikpik"

            # Commande pour changer de personnalité manuellement
            if message_lower in ["!personality", "!change", "!nova"] and is_owner:
                response = await self._trigger_personality_change(username)
                if response:
                    await self._send_response(response)
                return True

            # Commande pour voir les stats de personnalité
            elif message_lower in ["!stats", "!persona"] and is_owner:
                response = self._get_personality_stats()
                await self._send_response(response)
                return True

            # Commande pour simuler un follow (test)
            elif message_lower.startswith("!testfollow") and is_owner:
                parts = message.split()
                test_user = parts[1] if len(parts) > 1 else "TestUser"
                response = await self._simulate_follow(test_user)
                if response:
                    await self._send_response(response)
                return True

            # Commande pour simuler un sub (test)
            elif message_lower.startswith("!testsub") and is_owner:
                parts = message.split()
                test_user = parts[1] if len(parts) > 1 else "TestSubscriber"
                response = await self._simulate_subscription(test_user)
                if response:
                    await self._send_response(response)
                return True

            return False

        except Exception as e:
            logger.error(f"Erreur lors du traitement des commandes spéciales: {e}")
            return False

    async def _handle_persona_commands(
        self, username: str, message: str, message_lower: str
    ) -> bool:
        """Gère les commandes publiques liées aux personnalités"""
        if not self.ai_handler or not self.ai_handler.is_initialized:
            return False

        if not message_lower.startswith("!persona"):
            return False

        parts = message.strip().split()
        if len(parts) == 1 or parts[1].lower() == "list":
            overview = self.ai_handler.list_personalities()
            if not overview:
                await self._send_response("🤖 Aucune personnalité trouvée.")
                return True

            items = []
            for persona in overview:
                emoji = persona.get("emoji", "🎭")
                tone = persona.get("tone")
                tone_suffix = f" · ton: {tone}" if tone else ""
                items.append(
                    f"{emoji} {persona['type']} ({persona['name']}){tone_suffix}"
                )
            overview_text = " | ".join(items)
            await self._send_response(
                f"🎭 Personnalités disponibles: {overview_text}\nUtilise '!persona preview <type>' pour plus de détails."
            )
            return True

        if parts[1].lower() == "preview":
            if len(parts) < 3:
                await self._send_response("🤖 Utilisation: !persona preview <type/nom>")
                return True

            identifier = " ".join(parts[2:])
            preview = self.ai_handler.get_personality_preview(identifier)
            if not preview:
                await self._send_response(
                    f"🤖 Aucune personnalité trouvée pour '{identifier}'."
                )
                return True

            emoji = preview.get("emoji", "🎭")
            tone = preview.get("tone", "")
            tone_line = f"Ton: {tone}\n" if tone else ""
            catchphrases = preview.get("catchphrases", [])
            catchphrases_line = (
                "\n".join(f"- {phrase}" for phrase in catchphrases)
                if catchphrases
                else ""
            )
            commands = preview.get("commands", [])
            commands_line = f"Commandes: {', '.join(commands)}\n" if commands else ""
            keywords = preview.get("keywords", [])
            keywords_line = f"Mots-clés: {', '.join(keywords)}\n" if keywords else ""
            sample_prompts = preview.get("sample_prompts", [])
            sample_line = (
                f"Prompts suggérés: {', '.join(sample_prompts)}\n"
                if sample_prompts
                else ""
            )
            cooldown = preview.get("cooldown", 0)

            preview_message = (
                f"{emoji} {preview['name']} ({preview['type']})\n"
                f"{preview['description']}\n"
                f"{tone_line}"
                f"Cooldown: {cooldown}s\n"
                f"{commands_line}{keywords_line}{sample_line}{catchphrases_line}"
            ).strip()

            await self._send_response(preview_message)
            return True

        return False

    async def _trigger_personality_change(self, username: str) -> Optional[str]:
        """
        Déclenche un changement de personnalité manuel

        Args:
            username: Utilisateur qui a déclenché la commande

        Returns:
            str: Message de confirmation ou None
        """
        try:
            # Simuler un événement manuel via le chat handler
            if hasattr(self, "chat_handler_ref"):
                return await self.chat_handler_ref.trigger_manual_personality_change()
            else:
                # Fallback direct avec l'AI handler
                if self.ai_handler:
                    announcement = self.ai_handler.change_personality()
                    return f"🎲 {username} a déclenché un changement ! {announcement}"

            return f"@{username} Impossible de changer de personnalité pour le moment !"

        except Exception as e:
            logger.error(f"Erreur lors du changement de personnalité manuel: {e}")
            return f"@{username} Erreur lors du changement de personnalité !"

    def _get_personality_stats(self) -> str:
        """
        Récupère les statistiques de personnalité

        Returns:
            str: Message avec les stats
        """
        try:
            if self.ai_handler:
                current_name = self.ai_handler.get_current_personality_name()
                stats = self.ai_handler.get_personality_stats()

                history = ", ".join(stats.get("history", [])[-3:])  # 3 dernières

                return f"🎭 Personnalité actuelle: {current_name} | Historique récent: {history}"

            return "🤖 Impossible de récupérer les stats de personnalité"

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return "🤖 Erreur lors de la récupération des stats"

    async def _simulate_follow(self, test_user: str) -> Optional[str]:
        """
        Simule un follow pour tester le système

        Args:
            test_user: Nom de l'utilisateur de test

        Returns:
            str: Message de test ou None
        """
        try:
            if (
                hasattr(self, "chat_handler_ref")
                and self.chat_handler_ref.event_handler
            ):
                return await self.chat_handler_ref.event_handler.handle_follow(
                    test_user
                )

            return f"🎭 Test follow simulé pour {test_user} (système d'événements non disponible)"

        except Exception as e:
            logger.error(f"Erreur lors de la simulation de follow: {e}")
            return None

    async def _simulate_subscription(self, test_user: str) -> Optional[str]:
        """
        Simule un sub pour tester le système

        Args:
            test_user: Nom de l'utilisateur de test

        Returns:
            str: Message de test ou None
        """
        try:
            if (
                hasattr(self, "chat_handler_ref")
                and self.chat_handler_ref.event_handler
            ):
                return await self.chat_handler_ref.event_handler.handle_subscription(
                    test_user
                )

            return f"🎭 Test sub simulé pour {test_user} (système d'événements non disponible)"

        except Exception as e:
            logger.error(f"Erreur lors de la simulation de sub: {e}")
            return None

    def set_chat_handler_reference(self, chat_handler):
        """
        Définit une référence vers le chat handler pour accéder aux événements

        Args:
            chat_handler: Instance du chat handler
        """
        self.chat_handler_ref = chat_handler
        logger.info("Référence vers chat handler configurée")

    async def _generate_ai_response(
        self, username: str, message: str, is_owner: bool, trigger_reason: str
    ) -> Optional[str]:
        """
        Génère une réponse avec l'IA

        Args:
            username: Nom de l'utilisateur
            message: Message nettoyé
            is_owner: True si c'est le propriétaire
            trigger_reason: Raison du déclenchement

        Returns:
            str: Réponse générée ou None
        """
        try:
            if not self.ai_handler or not self.ai_handler.is_initialized:
                logger.error("Gestionnaire IA non disponible")
                return f"@{username} Mon cerveau est en maintenance... 🤖"

            # Générer la réponse selon le contexte
            if trigger_reason == "owner_message":
                # Réponse spéciale pour le propriétaire
                response = await self.ai_handler.process_message(
                    username=username, message=message, is_owner=True
                )
            else:
                # Réponse normale pour les mentions
                response = await self.ai_handler.process_message(
                    username=username, message=message, is_owner=False
                )

            return response

        except Exception as e:
            logger.error(f"Erreur lors de la génération IA: {e}")
            return f"@{username} Erreur système... comme tes skills ! 😏"

    async def _send_response(self, response: str):
        """
        Envoie la réponse via le callback

        Args:
            response: Réponse à envoyer
        """
        try:
            if self.response_callback:
                if asyncio.iscoroutinefunction(self.response_callback):
                    await self.response_callback(response)
                else:
                    self.response_callback(response)
                logger.info(f"Réponse envoyée: {response}")
            else:
                logger.warning("Pas de callback pour envoyer la réponse")

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de la réponse: {e}")

    def set_response_callback(self, callback: Callable):
        """
        Définit le callback pour envoyer les réponses

        Args:
            callback: Fonction pour envoyer les messages
        """
        self.response_callback = callback
        logger.info("Callback de réponse configuré")

    async def start_processing_queue(self):
        """Démarre le traitement de la queue de messages"""
        self.processing = True
        logger.info("Démarrage du traitement de la queue")

        while self.processing:
            try:
                # Attendre un message dans la queue
                username, message = await asyncio.wait_for(
                    self.message_queue.get(), timeout=1.0
                )

                # Traiter le message
                await self.process_message(username, message)

                # Marquer la tâche comme terminée
                self.message_queue.task_done()

            except asyncio.TimeoutError:
                # Timeout normal, continuer la boucle
                continue
            except Exception as e:
                logger.error(f"Erreur dans la queue de traitement: {e}")

    async def add_message_to_queue(self, username: str, message: str):
        """
        Ajoute un message à la queue de traitement

        Args:
            username: Nom de l'utilisateur
            message: Contenu du message
        """
        await self.message_queue.put((username, message))

    def stop_processing(self):
        """Arrête le traitement de la queue"""
        self.processing = False
        logger.info("Arrêt du traitement de la queue")

    def get_status(self) -> dict:
        """
        Retourne le statut du processeur

        Returns:
            dict: Informations de statut
        """
        return {
            "processing": self.processing,
            "queue_size": self.message_queue.qsize(),
            "ai_handler_ready": self.ai_handler is not None
            and self.ai_handler.is_initialized,
            "response_callback_set": self.response_callback is not None,
        }

    def _check_personality_triggers(self, message: str) -> Optional[str]:
        """Détecte les triggers personnalisés de la personnalité active"""
        if not self.ai_handler or not self.ai_handler.is_initialized:
            return None

        triggers = self.ai_handler.get_current_triggers()
        message_lower = message.lower()

        for command in triggers.get("commands", []):
            if message_lower.startswith(command):
                return f"personality_command:{command}"

        for keyword in triggers.get("keywords", []):
            if keyword in message_lower:
                return f"personality_keyword:{keyword}"

        return None
