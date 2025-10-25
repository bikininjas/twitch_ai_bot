"""
Tests unitaires pour les changements de personnalité
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from gemini_ai.response_generator import GeminiResponseGenerator  # type: ignore


class DummyPersonalityManager:
    """PersonalityManager factice pour simuler les changements"""

    def __init__(self):
        self.force_calls = 0
        self.manual_calls = 0
        self.current_name = "nova_the_test_cat"

    def change_personality(self, new_personality=None, force: bool = False):
        if force:
            self.force_calls += 1
            self.current_name = "nova_the_forced_cat"
            return True, "🎭 Personnalité forcée !"
        self.manual_calls += 1
        return False, "⏰ Changement de personnalité en cooldown !"

    def get_current_personality_name(self):
        return self.current_name


def test_manual_vs_forced_change():
    """Vérifie la prise en compte du tuple (succès, annonce)"""
    generator = object.__new__(GeminiResponseGenerator)
    generator.personality_manager = DummyPersonalityManager()

    manual_message = generator.change_personality(force=False)
    assert manual_message.startswith("⏰")

    forced_message = generator.change_personality(force=True)
    assert forced_message.startswith("🎭")

    # S'assurer que le gestionnaire factice a été utilisé comme prévu
    assert generator.personality_manager.manual_calls == 1
    assert generator.personality_manager.force_calls == 1


def run_tests():
    try:
        test_manual_vs_forced_change()
        print("✅ Tests de personnalités (manual/force) réussis")
        return True
    except AssertionError as exc:
        print(f"❌ Test de personnalités échoué: {exc}")
        return False
    except Exception as exc:
        print(f"❌ Erreur inattendue: {exc}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
