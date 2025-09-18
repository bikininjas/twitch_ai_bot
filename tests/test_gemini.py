"""
Test de connexion pour l'API Gemini
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.append(str(Path(__file__).parent.parent / "src"))

import asyncio
import logging
from gemini_ai.config import GeminiConfig
from gemini_ai.ai_handler import GeminiHandler

def test_gemini_connection():
    """Test la connexion à l'API Gemini"""
    print("🧠 Test de connexion à Gemini AI...")
    
    try:
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        
        # Test de la configuration
        print("📋 Test de la configuration...")
        config = GeminiConfig()
        print("✅ Configuration Gemini chargée")
        
        # Test de connexion basique
        print("🔗 Test de connexion basique...")
        if config.test_connection():
            print("✅ Connexion Gemini réussie")
        else:
            print("❌ Échec de la connexion Gemini")
            return False
        
        # Test du gestionnaire IA
        print("🤖 Test du gestionnaire IA...")
        ai_handler = GeminiHandler()
        if ai_handler.initialize():
            print("✅ Gestionnaire IA initialisé")
        else:
            print("❌ Échec d'initialisation du gestionnaire IA")
            return False
        
        # Test de génération de réponse
        print("💬 Test de génération de réponse...")
        response = asyncio.run(ai_handler.process_message(
            username="testuser",
            message="Hello bot, how are you?",
            is_owner=False
        ))
        
        if response:
            print(f"✅ Réponse générée: {response}")
        else:
            print("❌ Aucune réponse générée")
            return False
        
        print("🎉 Tous les tests Gemini ont réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test Gemini: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_connection()
    if not success:
        sys.exit(1)
    print("✅ Test Gemini terminé avec succès")