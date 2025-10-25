"""Gestionnaire de personnalités multiples pour nova_the_red_cat."""

import logging
import os
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .personality_schema import PersonalityConfig
from .personality_store import (
    BasePersonalityStore,
    JsonPersonalityStore,
    build_store,
)

logger = logging.getLogger(__name__)


@dataclass
class Personality:
    """Définition d'une personnalité"""

    name: str
    type: str
    description: str
    cultural_figure: str
    prompt_base: str
    signature: str
    announcement_variants: List[str]
    color_emoji: str
    catchphrases: List[str]
    tone: Optional[str] = None
    triggers_keywords: List[str] = field(default_factory=list)
    triggers_commands: List[str] = field(default_factory=list)
    sample_prompts: List[str] = field(default_factory=list)
    cooldown_override: Optional[int] = None
    schema_version: int = 1


class PersonalityManager:
    """Gestionnaire des personnalités multiples du bot."""

    def __init__(
        self,
        cooldown_time: int = 300,
        store: Optional[BasePersonalityStore] = None,
        storage_options: Optional[dict] = None,
    ):
        self.default_cooldown = cooldown_time
        self.cooldown_time = cooldown_time
        self.store = store or build_store(storage_options)
        self.personalities: Dict[str, Personality] = self._load_personalities()
        self.current_personality: Optional[Personality] = None
        self.last_change_time = 0.0
        self.personality_history: List[str] = []
        self._set_default_personality()

    def _load_personalities(self) -> Dict[str, Personality]:
        """Charge les personnalités depuis le backend configuré."""
        try:
            raw_personalities = self.store.load()
        except Exception as exc:
            logger.error(
                "Erreur lors du chargement des personnalités (%s). Retour au JSON local.",
                exc,
            )
            self.store = JsonPersonalityStore(
                os.path.join(os.path.dirname(__file__), "personalities")
            )
            raw_personalities = self.store.load()

        if not raw_personalities:
            logger.warning("Aucune personnalité trouvée dans le backend actif")
            return self._get_default_personality()

        personalities: Dict[str, Personality] = {}
        for personality_type, config in raw_personalities.items():
            try:
                personalities[personality_type] = self._build_personality(
                    personality_type, config
                )
            except Exception as exc:
                logger.error(
                    "Impossible de construire la personnalité %s: %s",
                    personality_type,
                    exc,
                )

        if not personalities:
            logger.warning(
                "Toutes les personnalités ont échoué à la construction. Fallback par défaut."
            )
            return self._get_default_personality()

        logger.info(
            "Chargé %d personnalités depuis le backend actif", len(personalities)
        )
        return personalities

    def _build_personality(
        self, personality_type: str, config: PersonalityConfig
    ) -> Personality:
        announcement_variants = config.announcement_variants or [
            f"{config.emoji} {phrase} ! Mode gaming activé ! {config.emoji}"
            for phrase in config.iconic_phrases[:3]
        ]

        signature = config.signature or f"- nova {config.emoji}"

        prompt_sections = [
            f"Tu es {config.name}, un bot Twitch qui parle comme {config.cultural_figure} !",
            "IMPORTANT : Tu DOIS répondre en FRANÇAIS uniquement, SAUF pour :",
            "- Les expressions gamers universelles (GG, noob, etc.)",
            "- Le jargon Twitch/internet (POGGERS, KEKW, etc.)",
            "",
            f"Utilise les expressions iconiques : {', '.join(config.iconic_phrases)}",
            "",
            "STYLE DE RÉPONSE :",
            "- Phrases courtes et complètes (toujours bien terminées)",
            "- Maximum 400 caractères au total",
            "- Termine par de la ponctuation (. ! ?)",
            "- Évite les phrases trop longues",
        ]

        if config.tone:
            prompt_sections.append(f"- Ton recommandé : {config.tone}")

        prompt_base = "\n".join(prompt_sections)

        return Personality(
            name=config.name,
            type=personality_type,
            description=config.description,
            cultural_figure=config.cultural_figure,
            prompt_base=prompt_base,
            signature=signature,
            announcement_variants=announcement_variants,
            color_emoji=config.emoji,
            catchphrases=config.iconic_phrases,
            tone=config.tone,
            triggers_keywords=[kw.lower() for kw in config.triggers.keywords],
            triggers_commands=[cmd.lower() for cmd in config.triggers.commands],
            sample_prompts=config.sample_prompts,
            cooldown_override=config.cooldown_override,
            schema_version=config.schema_version,
        )

    def _get_default_personality(self) -> Dict[str, Personality]:
        """Retourne une personnalité par défaut en cas d'erreur"""
        default = Personality(
            name="nova_the_red_cat",
            type="sarcastic",
            description="Le chat rouge sarcastique par défaut",
            cultural_figure="Nova",
            prompt_base="""Tu es nova_the_red_cat, un bot Twitch sarcastique et humoristique.

IMPORTANT : Tu DOIS répondre en FRANÇAIS uniquement, SAUF pour :
- Les expressions gamers universelles (GG, noob, etc.)
- Le jargon Twitch/internet (KEKW, Pogchamp, etc.)

STYLE DE RÉPONSE :
- Phrases courtes et complètes (toujours bien terminées)
- Maximum 400 caractères au total
- Termine par de la ponctuation (. ! ?)
- Sois sarcastique mais amusant !""",
            signature="- nova 🐱",
            announcement_variants=[
                "🎭 Mode sarcasme activé ! Préparez-vous aux vannes ! 😏"
            ],
            color_emoji="🔴",
            catchphrases=["Oh regarde qui parle...", "Tiens tiens..."],
            tone="Sarcastique mais joueur",
            triggers_keywords=["nova", "sarcasme"],
            triggers_commands=["!nova"],
            sample_prompts=["Insulte affectueusement un viewer"],
            cooldown_override=None,
            schema_version=1,
        )
        return {"sarcastic": default}

    def _set_default_personality(self):
        """Définit la personnalité par défaut"""
        if self.personalities:
            default_key = (
                "sarcastic"
                if "sarcastic" in self.personalities
                else list(self.personalities.keys())[0]
            )
            self.current_personality = self.personalities[default_key]
            logger.info(f"Personnalité par défaut : {self.current_personality.name}")

    def get_random_personality(self, exclude_current: bool = True) -> Personality:
        """Sélectionne une personnalité aléatoire"""
        available = list(self.personalities.values())
        if exclude_current and self.current_personality:
            available = [
                p for p in available if p.type != self.current_personality.type
            ]
        if available:
            return random.choice(available)
        if self.current_personality:
            return self.current_personality
        # Dernier recours : retourner la première personnalité disponible
        return next(iter(self.personalities.values()))

    def change_personality(
        self, new_personality: Optional[str] = None, force: bool = False
    ) -> Tuple[bool, str]:
        """Change la personnalité du bot avec système de cooldown"""
        current_time = time.time()

        if not force and (current_time - self.last_change_time) < self.cooldown_time:
            remaining = int(self.cooldown_time - (current_time - self.last_change_time))
            return (
                False,
                f"⏰ Changement de personnalité en cooldown ! Encore {remaining} secondes...",
            )

        if new_personality and new_personality in self.personalities:
            personality = self.personalities[new_personality]
        else:
            personality = self.get_random_personality()

        if (
            not force
            and self.current_personality
            and personality.type == self.current_personality.type
        ):
            personality = self.get_random_personality()

        old_personality = (
            self.current_personality.name if self.current_personality else "aucune"
        )
        self.current_personality = personality
        self.last_change_time = current_time
        self.cooldown_time = personality.cooldown_override or self.default_cooldown
        self.personality_history.append(personality.type)

        if len(self.personality_history) > 10:
            self.personality_history = self.personality_history[-10:]

        announcement = random.choice(personality.announcement_variants)
        logger.info(
            f"Changement de personnalité : {old_personality} -> {personality.name}"
        )

        return True, announcement

    def get_current_prompt(self) -> str:
        """Retourne le prompt de la personnalité actuelle"""
        if not self.current_personality:
            self._set_default_personality()
        return self.current_personality.prompt_base if self.current_personality else ""

    def get_current_signature(self) -> str:
        """Retourne la signature de la personnalité actuelle"""
        if not self.current_personality:
            self._set_default_personality()
        return (
            self.current_personality.signature
            if self.current_personality
            else "- nova 🐱"
        )

    def get_current_personality_name(self) -> str:
        """Retourne le nom de la personnalité actuelle"""
        if not self.current_personality:
            self._set_default_personality()
        return (
            self.current_personality.name
            if self.current_personality
            else "nova_the_red_cat"
        )

    def get_startup_message(self) -> str:
        """Génère un message de démarrage avec la personnalité actuelle"""
        if not self.current_personality:
            self._set_default_personality()

        if self.current_personality:
            announcement = random.choice(self.current_personality.announcement_variants)
            return f"🤖 {self.current_personality.name} est connecté ! {announcement}"
        else:
            return "🤖 nova_the_red_cat est connecté !"

    def get_personality_stats(self) -> Dict:
        """Retourne les statistiques des personnalités"""
        return {
            "current": (
                self.current_personality.name if self.current_personality else None
            ),
            "available_count": len(self.personalities),
            "history": self.personality_history[-5:],
            "all_personalities": [p.name for p in self.personalities.values()],
        }

    def force_personality(self, personality_type: str) -> Tuple[bool, str]:
        """Force un changement de personnalité sans cooldown"""
        return self.change_personality(personality_type, force=True)

    def get_random_catchphrase(self) -> str:
        """Retourne une phrase iconique aléatoire de la personnalité actuelle"""
        if not self.current_personality:
            self._set_default_personality()

        if self.current_personality and self.current_personality.catchphrases:
            return random.choice(self.current_personality.catchphrases)
        return "Oh regarde qui parle..."

    def get_personality_signature(self) -> str:
        """Alias pour get_current_signature pour compatibilité"""
        return self.get_current_signature()

    def list_personalities(self) -> List[Dict[str, str]]:
        """Retourne une liste résumée des personnalités disponibles"""
        overview = []
        for key, personality in self.personalities.items():
            overview.append(
                {
                    "type": key,
                    "name": personality.name,
                    "emoji": personality.color_emoji,
                    "tone": personality.tone,
                    "description": personality.description,
                }
            )
        return overview

    def get_personality_preview(self, identifier: str) -> Optional[Dict[str, object]]:
        """Retourne les détails d'une personnalité pour la commande preview"""
        identifier_lower = identifier.lower()

        # Recherche par type
        if identifier_lower in self.personalities:
            personality = self.personalities[identifier_lower]
        else:
            # Recherche par nom
            personality = next(
                (
                    p
                    for p in self.personalities.values()
                    if p.name.lower() == identifier_lower
                ),
                None,
            )

        if not personality:
            return None

        return {
            "type": personality.type,
            "name": personality.name,
            "emoji": personality.color_emoji,
            "description": personality.description,
            "tone": personality.tone,
            "catchphrases": personality.catchphrases[:3],
            "commands": personality.triggers_commands,
            "keywords": personality.triggers_keywords,
            "sample_prompts": personality.sample_prompts[:3],
            "cooldown": personality.cooldown_override or self.default_cooldown,
        }

    def get_current_triggers(self) -> Dict[str, List[str]]:
        """Retourne les triggers de la personnalité actuelle"""
        if not self.current_personality:
            self._set_default_personality()
        if not self.current_personality:
            return {"keywords": [], "commands": []}
        return {
            "keywords": self.current_personality.triggers_keywords,
            "commands": self.current_personality.triggers_commands,
        }

    def get_current_tone(self) -> Optional[str]:
        if not self.current_personality:
            self._set_default_personality()
        return self.current_personality.tone if self.current_personality else None

    def get_current_sample_prompts(self) -> List[str]:
        if not self.current_personality:
            self._set_default_personality()
        if not self.current_personality:
            return []
        return self.current_personality.sample_prompts
