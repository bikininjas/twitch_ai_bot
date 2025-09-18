#!/usr/bin/env python3
"""
Script de lancement du bot en background avec monitoring
"""

import subprocess
import sys
import time
import signal
from pathlib import Path

def run_bot_background():
    """Lance le bot en arrière-plan et monitore les logs"""
    print("🚀 Lancement du bot Twitch AI en arrière-plan...")
    
    # Chemin vers le projet
    project_dir = Path(__file__).parent
    bot_script = project_dir / "src" / "main.py"
    venv_python = project_dir / "venv" / "bin" / "python3"
    
    # Vérifier que l'environnement virtuel existe
    if not venv_python.exists():
        print("❌ Environnement virtuel non trouvé. Exécutez d'abord:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        return
    
    try:
        # Lancer le bot en arrière-plan
        process = subprocess.Popen(
            [str(venv_python), str(bot_script)],
            cwd=str(project_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print(f"✅ Bot lancé avec PID: {process.pid}")
        print("📝 Logs en temps réel:")
        print("-" * 50)
        
        # Monitorer les logs en temps réel
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        return_code = process.poll()
        if return_code != 0:
            print(f"❌ Le bot s'est arrêté avec le code d'erreur: {return_code}")
        else:
            print("✅ Bot arrêté normalement")
            
    except KeyboardInterrupt:
        print("\\n🛑 Arrêt demandé par l'utilisateur")
        if 'process' in locals():
            process.terminate()
            process.wait()
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def show_logs():
    """Affiche les derniers logs du bot"""
    logs_dir = Path(__file__).parent / "logs"
    
    if not logs_dir.exists():
        print("❌ Dossier de logs non trouvé")
        return
    
    # Trouver le fichier de log le plus récent
    log_files = list(logs_dir.glob("bot_*.log"))
    if not log_files:
        print("❌ Aucun fichier de log trouvé")
        return
    
    latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
    
    print(f"📋 Affichage des logs: {latest_log.name}")
    print("-" * 50)
    
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Afficher les 50 dernières lignes
            for line in lines[-50:]:
                print(line.rstrip())
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des logs: {e}")

def main():
    """Point d'entrée principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "logs":
            show_logs()
            return
        elif sys.argv[1] == "help":
            print("🤖 Bot Twitch AI - Commandes:")
            print("  python3 run_bot.py        - Lance le bot")
            print("  python3 run_bot.py logs   - Affiche les logs")
            print("  python3 run_bot.py help   - Affiche cette aide")
            return
    
    run_bot_background()

if __name__ == "__main__":
    main()