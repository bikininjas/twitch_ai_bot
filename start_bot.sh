#!/bin/bash
"""
Script de lancement du bot en background avec monitoring
"""

cd /home/seb/GITRepos/twitch_ai_bot

echo "🚀 Lancement du bot Twitch AI en background..."

# Activer l'environnement virtuel et lancer le bot
source venv/bin/activate
nohup python3 src/main.py > /dev/null 2>&1 &

# Récupérer le PID
BOT_PID=$!
echo "📊 Bot lancé avec PID: $BOT_PID"

# Sauvegarder le PID pour pouvoir l'arrêter plus tard
echo $BOT_PID > bot.pid

# Attendre un peu et vérifier le dernier log
sleep 3

echo "📋 Logs récents:"
echo "=================="

# Afficher le dernier fichier de log créé
LATEST_LOG=$(ls -t logs/bot_*.log 2>/dev/null | head -1)

if [ -n "$LATEST_LOG" ]; then
    echo "📄 Fichier de log: $LATEST_LOG"
    echo ""
    tail -20 "$LATEST_LOG"
else
    echo "❌ Aucun fichier de log trouvé"
fi

echo ""
echo "🔍 Pour voir les logs en temps réel:"
echo "tail -f logs/\$(ls -t logs/bot_*.log | head -1)"
echo ""
echo "🛑 Pour arrêter le bot:"
echo "kill \$(cat bot.pid)"