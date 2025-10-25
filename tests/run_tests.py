#!/usr/bin/env python3
"""
Script de test global pour le bot Twitch AI
"""

import sys
import os
from pathlib import Path


def run_tests():
    """Exécute tous les tests"""
    print("🧪 Lancement des tests du Bot Twitch AI")
    print("=" * 50)

    # Définir les tests à exécuter
    tests = [
        ("test_functionality.py", "Tests de fonctionnalité"),
        ("test_twitch.py", "Tests de connexion Twitch"),
        ("test_gemini.py", "Tests de connexion Gemini"),
        ("test_authentication.py", "Tests d'authentification complets"),
        ("test_personality_manager.py", "Tests de personnalités"),
    ]
    test_dir = Path(__file__).parent
    results = []

    for test_file, description in tests:
        print(f"\\n🔍 {description}...")
        test_path = test_dir / test_file

        if not test_path.exists():
            print(f"❌ Fichier de test manquant: {test_file}")
            results.append(False)
            continue

        try:
            # Exécuter le test
            exit_code = os.system(f"python3 {test_path}")

            if exit_code == 0:
                print(f"✅ {description} réussis")
                results.append(True)
            else:
                print(f"❌ {description} échoués")
                results.append(False)

        except Exception as e:
            print(f"❌ Erreur lors de l'exécution de {test_file}: {e}")
            results.append(False)

    # Résumé
    print("\\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)

    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests

    for i, (test_file, description) in enumerate(tests):
        status = "✅ RÉUSSI" if results[i] else "❌ ÉCHOUÉ"
        print(f"{description}: {status}")

    print(
        f"\\nTotal: {total_tests} | Réussis: {passed_tests} | Échoués: {failed_tests}"
    )

    if all(results):
        print("\\n🎉 TOUS LES TESTS ONT RÉUSSI!")
        print("🚀 Le bot est prêt à être lancé avec: python3 bot.py")
        return True
    else:
        print("\\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez votre configuration et les dépendances")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
