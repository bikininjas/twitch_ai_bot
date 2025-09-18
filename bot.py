#!/usr/bin/env python3
"""
Script de lancement du bot Twitch AI
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier src au path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from main import main
    import asyncio
    
    if __name__ == "__main__":
        print("🤖 Lancement du Bot Twitch AI...")
        asyncio.run(main())
        
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("💡 Assurez-vous d'avoir installé les dépendances avec: pip install -r requirements.txt")
    sys.exit(1)
except KeyboardInterrupt:
    print("\\n👋 Arrêt du bot par l'utilisateur")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)