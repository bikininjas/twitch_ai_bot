"""
Classes de base pour le système de personnalités
"""

from dataclasses import dataclass
from enum import Enum
from typing import List

class PersonalityType(Enum):
    """Types de personnalités disponibles"""
    SARCASTIC = "sarcastique"
    MACRON = "macron"
    JCVD = "jcvd"
    DICTATOR = "dictateur"
    MELENCHON = "melenchon"
    TAZ = "taz"
    DIABLE = "diable"
    JUL = "jul"

@dataclass
class Personality:
    """Définition d'une personnalité"""
    name: str
    type: PersonalityType
    description: str
    prompt_base: str
    signature: str
    announcement_variants: List[str]
    color_emoji: str
    catchphrases: List[str]