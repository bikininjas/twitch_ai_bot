"""
Package des personnalités pour nova_the_red_cat
"""

from .base import Personality, PersonalityType
from .sarcastic import create_sarcastic_personality
from .macron import create_macron_personality
from .jcvd import create_jcvd_personality
from .dictator import create_dictator_personality
from .melenchon import create_melenchon_personality
from .taz import create_taz_personality
from .diable import create_diable_personality
from .jul import create_jul_personality

# Factory pour créer toutes les personnalités
def create_all_personalities() -> dict[PersonalityType, Personality]:
    """Crée toutes les personnalités disponibles"""
    personalities = {}
    
    personalities[PersonalityType.SARCASTIC] = create_sarcastic_personality()
    personalities[PersonalityType.MACRON] = create_macron_personality()
    personalities[PersonalityType.JCVD] = create_jcvd_personality()
    personalities[PersonalityType.DICTATOR] = create_dictator_personality()
    personalities[PersonalityType.MELENCHON] = create_melenchon_personality()
    personalities[PersonalityType.TAZ] = create_taz_personality()
    personalities[PersonalityType.DIABLE] = create_diable_personality()
    personalities[PersonalityType.JUL] = create_jul_personality()
    
    return personalities

__all__ = [
    'Personality',
    'PersonalityType', 
    'create_all_personalities',
    'create_sarcastic_personality',
    'create_macron_personality',
    'create_jcvd_personality',
    'create_dictator_personality',
    'create_melenchon_personality',
    'create_taz_personality',
    'create_diable_personality',
    'create_jul_personality'
]