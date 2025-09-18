# 🤖 Nova Bot Manager

Gestionnaire de processus interactif pour nova_the_red_cat Twitch Bot avec interface en ligne de commande colorée et fonctionnalités de monitoring en temps réel.

## 🚀 Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/bikininjas/twitch_ai_bot.git
cd twitch_ai_bot

# Lancer l'installation automatique
./install.sh
```

## 📋 Fonctionnalités

### 🎛️ **Gestion de Processus**
- ✅ **Démarrage en arrière-plan** - Le bot tourne indépendamment du terminal
- ✅ **Arrêt propre** - Fermeture gracieuse avec fallback forcé
- ✅ **Redémarrage intelligent** - Arrêt + démarrage automatique
- ✅ **Monitoring PID** - Suivi du processus avec fichier PID

### 📊 **Monitoring et Logs**
- ✅ **Logs en temps réel** - `tail -f` intégré avec interface colorée
- ✅ **Historique des logs** - Affichage des dernières entrées
- ✅ **Statut en direct** - Uptime, PID, état du processus
- ✅ **Rotation automatique** - Logs horodatés avec headers

### 🎨 **Interface Utilisateur**
- ✅ **Menu interactif** coloré avec émojis
- ✅ **Mode ligne de commande** pour scripts et automation
- ✅ **Codes couleur** pour statuts (vert=ok, rouge=erreur, etc.)
- ✅ **Interface responsive** - Actualisation automatique

### 🔧 **Configuration Avancée**
- ✅ **Variables d'environnement** via fichier `.env`
- ✅ **Chemins configurables** pour logs et fichiers PID
- ✅ **Alias shell** optionnel (`nova` command)
- ✅ **Installation guidée** avec vérifications

## 📖 Utilisation

### Mode Interactif (Recommandé)
```bash
./bot_manager.sh
# ou simplement:
./bot_manager.sh menu
```

**Interface du menu :**
```
╔════════════════════════════════════════════════════════════════════════════╗
║                          🤖 NOVA BOT MANAGER 🤖                              ║
║              Script de gestion pour nova_the_red_cat Twitch Bot             ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ Status: nova_the_red_cat est EN COURS D'EXÉCUTION
ℹ️ PID: 12345
ℹ️ Uptime: 02:34:56
ℹ️ Log file: /path/to/logs/nova_bot.log

╔════════════════════════════════════════════════════════════════════════════╗
║                                   MENU                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

1. 🚀 Démarrer le bot
2. 🛑 Arrêter le bot  
3. 🔄 Redémarrer le bot
4. ℹ️ Voir les logs en temps réel
5. ℹ️ Voir les logs récents
6. 🔄 Actualiser le statut
0. ❌ Quitter

Votre choix: 
```

### Mode Ligne de Commande
```bash
# Démarrer le bot
./bot_manager.sh start

# Arrêter le bot
./bot_manager.sh stop

# Redémarrer le bot
./bot_manager.sh restart

# Vérifier le statut
./bot_manager.sh status

# Voir les logs en temps réel
./bot_manager.sh logs

# Voir les logs récents
./bot_manager.sh recent

# Aide
./bot_manager.sh help
```

### Avec Alias (après installation)
```bash
# Si vous avez configuré l'alias pendant l'installation
nova                # Mode interactif
nova start          # Démarrer
nova stop           # Arrêter
nova logs           # Logs temps réel
```

## 🔧 Configuration

### Fichier `.env`
```env
# Twitch Configuration
TWITCH_BOT_TOKEN=oauth:your_token_here
TWITCH_CHANNEL=your_channel_name
TWITCH_BOT_USERNAME=nova_the_red_cat

# Gemini AI Configuration  
GEMINI_API_KEY=your_gemini_api_key_here

# Bot Configuration
BOT_PERSONALITY_COOLDOWN=300
BOT_RESPONSE_DELAY=1
BOT_MAX_MESSAGE_LENGTH=200

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/nova_bot.log
```

### Variables du Script
```bash
# Dans bot_manager.sh, vous pouvez modifier:
BOT_SCRIPT="python3 -m src.main"       # Commande de lancement
PID_FILE="$HOME/.nova_bot.pid"         # Fichier PID
LOG_FILE="$PWD/logs/nova_bot.log"      # Fichier de logs
```

## 📁 Structure des Fichiers

```
twitch_ai_bot/
├── bot_manager.sh              # 🎛️ Gestionnaire principal
├── install.sh                  # 🚀 Script d'installation
├── .env                        # ⚙️ Configuration (à créer)
├── logs/
│   └── nova_bot.log           # 📋 Logs du bot
├── src/
│   ├── main.py               # 🤖 Point d'entrée du bot
│   └── ...                   # 📚 Code source
└── ~/.nova_bot.pid           # 🔍 Fichier PID (créé automatiquement)
```

## 🛠️ Dépannage

### Le bot ne démarre pas
```bash
# Vérifier les logs
./bot_manager.sh recent

# Vérifier la configuration
cat .env

# Tester le module Python
python3 -c "import src.main"
```

### Logs introuvables
```bash
# Créer le dossier logs
mkdir -p logs

# Vérifier les permissions
ls -la logs/
```

### PID file corrompu
```bash
# Nettoyer manuellement
rm -f ~/.nova_bot.pid

# Redémarrer le gestionnaire
./bot_manager.sh
```

### Processus zombie
```bash
# Forcer l'arrêt de tous les processus Python du bot
pkill -f "python3 -m src.main"

# Nettoyer le PID file
rm -f ~/.nova_bot.pid
```

## 🎯 Fonctionnalités Avancées

### Monitoring Automatique
Le script vérifie automatiquement l'état du processus et nettoie les fichiers PID obsolètes.

### Gestion d'Erreurs
- Arrêt gracieux avec timeout (10 secondes)
- Fallback sur `kill -9` si nécessaire
- Vérification de l'état avant toute opération

### Logging Enrichi
- Headers automatiques avec timestamps
- Séparation des sessions de bot
- Support du `tail -f` pour monitoring temps réel

### Interface Colorée
- Codes couleur pour statuts visuels
- Émojis pour meilleure lisibilité
- Formatage responsive selon la taille du terminal

## 🔗 Liens Utiles

- **Repository:** https://github.com/bikininjas/twitch_ai_bot
- **Gist des Personnalités:** https://gist.github.com/SebPikPik/291518241ab9743b0d16cd9cb589f04c
- **Documentation Twitch API:** https://dev.twitch.tv/docs/
- **Documentation Gemini API:** https://ai.google.dev/docs

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.