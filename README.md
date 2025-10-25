# 🤖 Twitch AI Bot

Un bot Twitch intelligent et sarcastique alimenté par Google Gemini AI qui interagit avec les utilisateurs dans le chat de votre chaîne.

## 🎯 Fonctionnalités

- **🤖 IA Sarcastique** : Réponses générées par Google Gemini avec une personnalité humoristique et sarcastique
- **🎮 Intégration Twitch** : Connexion IRC complète avec votre chaîne Twitch
- **👑 Interaction Privilégiée** : Répond automatiquement aux messages du propriétaire (`redpikpik`)
- **📢 Détection de Mentions** : Répond quand il est mentionné par d'autres utilisateurs
- **🎪 Jeux de Mots** : Créé des jeux de mots avec les pseudos des utilisateurs
- **⚡ Architecture Modulaire** : Code organisé par fonctionnalités dans des dossiers séparés
- **🔧 Gestionnaire de Bot** : Interface interactive pour contrôler le bot en background
- **🎭 Système de Personnalités** : 8 personnalités différentes avec configuration JSON
- **🗄️ Stockage Flex** : JSON versionné par défaut ou backend SQLite Cloud optionnel

## 🚀 Démarrage Rapide

### Installation Automatique

```bash
# Installation et configuration automatique
./install.sh
```

Le script crée l'environnement virtuel `.venv`, installe les dépendances et génère un fichier `.env` à partir de `.env.example`.

### Gestionnaire de Bot

```bash
# Lancer le gestionnaire interactif
./bot_manager.sh
```

Le gestionnaire de bot offre une interface interactive avec menu coloré pour :
- ✅ Démarrer le bot en arrière-plan
- ⏹️ Arrêter le bot proprement
- 🔄 Redémarrer le bot
- 📊 Voir le statut (PID, temps de fonctionnement)
- 📄 Afficher les logs en temps réel
- ⚙️ Configuration et aide

## 📂 Structure du Projet

```
twitch_ai_bot/
├── src/                          # Code source principal
│   ├── twitch_connection/        # Connexion et authentification Twitch
│   │   ├── auth.py              # Authentification Twitch
│   │   ├── irc_client.py        # Client IRC Twitch
│   │   └── message_handler.py   # Gestionnaire de messages
│   ├── gemini_ai/               # Intégration Google Gemini AI
│   │   ├── config.py            # Configuration Gemini
│   │   ├── response_generator.py # Générateur de réponses sarcastiques
│   │   └── ai_handler.py        # Gestionnaire principal IA
│   ├── chat_handler/            # Logique de gestion du chat
│   │   ├── mention_detector.py  # Détection des mentions et triggers
│   │   ├── message_processor.py # Processeur de messages
│   │   └── chat_manager.py      # Gestionnaire principal du chat
│   ├── utils/                   # Utilitaires et configuration
│   │   └── config.py            # Configuration et logging
│   └── main.py                  # Point d'entrée principal
├── tests/                       # Tests de connexion
│   ├── test_twitch.py          # Tests Twitch
│   ├── test_gemini.py          # Tests Gemini AI
│   ├── test_functionality.py   # Tests de fonctionnalité
│   └── run_tests.py            # Script de test global
├── bot_manager.sh              # Gestionnaire interactif du bot
├── install.sh                  # Script d'installation automatique
├── BOT_MANAGER_README.md       # Documentation du gestionnaire
├── src/gemini_ai/personalities/ # Personnalités JSON individuelles
├── .env                        # Variables d'environnement (à configurer)
├── .env.example                # Modèle d'environnement
├── .gitignore                  # Fichiers ignorés par Git
├── requirements.txt            # Dépendances Python
├── bot.py                      # Script de lancement simple
└── README.md                   # Cette documentation
```

## 🎭 Système de Personnalités

Le bot dispose de 8 personnalités distinctes configurées via les fichiers JSON du dossier `src/gemini_ai/personalities/` :

1. **👑 Nova the Red Cat** - Personnalité de base sarcastique
2. **🧙‍♂️ Gandalf** - Sage et mystérieux avec références LOTR
3. **🗡️ Jon Snow** - Noble et stoïque avec répliques GoT
4. **🤡 Joker** - Chaotique et imprévisible
5. **🏴‍☠️ Jack Sparrow** - Pirate charmeur et rusé
6. **🔬 Tony Stark** - Génie arrogant et technophile
7. **🗿 Stoic Marcus** - Philosophe stoïcien et sage
8. **🥷 Ninja Hattori** - Ninja mystérieux et agile

Chaque personnalité a ses propres :
- **Traits de caractère** uniques
- **Phrases iconiques** authentiques
- **Style de réponse** adapté
- **Références culturelles** appropriées

## 🛠️ Installation Manuelle

### 1. Prérequis

- **Python 3.8+** installé sur votre système
- **WSL Ubuntu** (pour votre cas d'usage)
- Accès à **Google AI Studio** pour l'API Gemini
- **Compte Twitch** avec bot configuré

### 2. Cloner le projet

```bash
git clone https://github.com/bikininjas/twitch_ai_bot.git
cd twitch_ai_bot
```

### 3. Créer l'environnement virtuel et installer les dépendances

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Configuration

#### Twitch Configuration

1. Allez sur [Twitch Developer Console](https://dev.twitch.tv/console)
2. Créez une nouvelle application
3. Notez votre **Client ID**
4. Générez un **OAuth Token** (utilisez [Twitch Token Generator](https://twitchtokengenerator.com/))

#### Google Gemini Configuration

1. Allez sur [Google AI Studio](https://aistudio.google.com/)
2. Créez une nouvelle clé API
3. Notez votre clé API Gemini

#### Fichier .env

Copiez le modèle `.env.example` puis éditez vos valeurs :

```bash
cp .env.example .env
```

Ensuite, modifiez le fichier `.env` à la racine du projet :

```env
# Twitch Bot Configuration
TWITCH_BOT_TOKEN=votre_token_oauth_twitch
TWITCH_BOT_CLIENT_ID=votre_client_id_twitch
TWITCH_CHANNEL=redpikpik
TWITCH_BOT_NAME=votre_nom_de_bot

# Google Gemini AI Configuration
GEMINI_API_KEY=votre_clé_api_gemini

# Bot Behavior Configuration
OWNER_USERNAME=redpikpik
BOT_PERSONALITY=sarcastic

# Logging
LOG_LEVEL=INFO
LOG_DIR=logs

# Personality Storage (optionnel)
#PERSONALITY_DB_URL=sqlitecloud://username:password@host:port/dbname
#PERSONALITY_DB_TABLE=personalities
#PERSONALITY_DB_TYPE_COLUMN=type
#PERSONALITY_DB_PAYLOAD_COLUMN=payload
```

## 🗄️ Backend de Personnalités (Optionnel)

Le bot charge ses personnalités depuis les fichiers JSON du dossier `src/gemini_ai/personalities/`.
Pour modifier les paramètres à chaud ou centraliser la configuration, vous pouvez fournir un
backend SQLite Cloud en renseignant `PERSONALITY_DB_URL` (et éventuellement les noms de table/colonnes).

- Si l'URL est définie et accessible, le bot lira les personnalités depuis SQLite Cloud.
- En cas d'erreur ou d'absence de configuration, il revient automatiquement aux fichiers JSON locaux.

Pour provisionner la table distante avec les JSON actuels :

```bash
python scripts/sync_personalities_to_db.py
```

Le script crée la table si besoin (`type` + `payload`) et effectue un `INSERT OR REPLACE`
pour chaque personnalité locale. Assurez-vous d'avoir installé `sqlitecloud` (déjà listé
dans `requirements.txt`) et défini `PERSONALITY_DB_URL` dans votre environnement.

La table attendue doit contenir au minimum deux colonnes :

| Colonne | Rôle | Exemple |
|---------|------|---------|
| `type`  | Identifiant unique de la personnalité | `sarcastic` |
| `payload` | Contenu JSON respectant le schéma `PersonalityConfig` | `{ "schema_version": 1, ... }` |

Les valeurs JSON doivent suivre le schéma défini dans `src/gemini_ai/personalities/README.md` (validé par Pydantic).

**⚠️ Important** : Ne partagez jamais votre fichier `.env` ! Il est déjà dans le `.gitignore`.

## 🧪 Tests

Avant de lancer le bot, testez les connexions :

```bash
# Tester toutes les fonctionnalités
python3 tests/run_tests.py

# Ou tester individuellement
python3 tests/test_twitch.py      # Test connexion Twitch
python3 tests/test_gemini.py      # Test connexion Gemini
python3 tests/test_functionality.py # Test fonctionnalités
```

## 🎮 Utilisation

### Gestionnaire de Bot (Recommandé)

```bash
# Interface interactive complète
./bot_manager.sh
```

Assurez-vous que l'environnement virtuel `.venv` est créé (via `./install.sh` ou `python3 -m venv .venv`) avant d'utiliser le gestionnaire : il lance le bot avec `.venv/bin/python`.

### Lancement Direct

```bash
# Méthode simple
python3 bot.py

# Ou directement
python3 src/main.py

# En arrière-plan avec logs
nohup python3 bot.py > logs/bot.log 2>&1 &
```

Activez d'abord l'environnement virtuel (`source .venv/bin/activate`) pour vous assurer que les bonnes dépendances et variables d'environnement sont utilisées.

### Comportement du Bot

Le bot réagit dans les situations suivantes :

#### 1. Messages du Propriétaire (redpikpik)
- **Quand** : À chaque message de `redpikpik`
- **Réponse** : Sarcastique mais respectueuse

```
redpikpik: Comment ça va ?
Bot: @redpikpik Ça va comme tes skills... en progression ! 😏
```

#### 2. Mentions Directes
- **Quand** : Le bot est mentionné par `@nom_du_bot` ou son nom
- **Réponse** : Sarcastique avec jeux de mots sur le pseudo

```
viewer123: @bot_name tu es là ?
Bot: @viewer123 Oui je suis là... contrairement à tes chances de win ! 💀
```

#### 3. Pas de Réponse
- Messages normaux des autres utilisateurs (sauf mention)

## 🔧 Gestionnaire de Bot - Fonctionnalités

### Interface Interactive

Le gestionnaire `bot_manager.sh` propose un menu coloré avec les options :

```
🤖 === NOVA THE RED CAT - BOT MANAGER ===

1. ▶️  Démarrer le bot
2. ⏹️  Arrêter le bot  
3. 🔄 Redémarrer le bot
4. 📊 Statut du bot
5. 📄 Voir les logs
6. ⚙️  Configuration
7. ❓ Aide
8. 🚪 Quitter
```

### Gestion des Processus

- **Démarrage** : Lance le bot en arrière-plan avec `nohup`
- **PID Tracking** : Sauvegarde du PID dans `logs/bot.pid`
- **Arrêt Gracieux** : Utilise `SIGTERM` puis `SIGKILL` si nécessaire
- **Monitoring** : Affichage du statut, temps de fonctionnement, utilisation CPU/mémoire

### Logs et Monitoring

- **Logs Centralisés** : Tous les logs dans `logs/bot.log`
- **Rotation** : Logs archivés automatiquement
- **Affichage Temps Réel** : `tail -f` intégré dans le gestionnaire
- **Filtering** : Options pour filtrer les logs par niveau

## 🛠️ Configuration Avancée

### Logging

Ajoutez ces variables à votre `.env` pour personnaliser les logs :

```env
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
LOG_DIR=logs               # Dossier de logs
```

### Personnalisation de la Personnalité

Modifiez `personalities_config.json` pour :
- Ajouter de nouvelles personnalités
- Modifier les traits existants
- Personnaliser les phrases iconiques
- Adapter les styles de réponse

## 🔧 Architecture Technique

### Modules Principaux

1. **twitch_connection** : Gère toute la communication avec Twitch IRC
   - Authentification OAuth
   - Connexion IRC persistante
   - Envoi/réception de messages

2. **gemini_ai** : Intégration avec Google Gemini
   - Configuration API
   - Génération de réponses personnalisées
   - Gestion des erreurs IA

3. **chat_handler** : Logique métier du chat
   - Détection des mentions
   - Processus de traitement des messages
   - Gestion des interactions

4. **utils** : Utilitaires transversaux
   - Configuration centralisée
   - Système de logging

### Flux de Traitement

```
Message Twitch → Détection Mention → IA Gemini → Réponse Chat
```

### Gestion des Processus

```
bot_manager.sh → nohup python3 bot.py → PID file → Monitoring
```

## 🚨 Dépannage

### Erreurs Communes

#### "Import could not be resolved"
```bash
# Vérifiez que vous êtes dans le bon dossier
cd twitch_ai_bot
python3 bot.py
```

#### "Identifiants Twitch invalides"
- Vérifiez votre token OAuth (doit commencer par `oauth:`)
- Vérifiez votre Client ID
- Assurez-vous que le bot a les permissions de modérateur

#### "Clé API Gemini manquante"
- Vérifiez votre clé API dans le fichier `.env`
- Testez avec `python3 tests/test_gemini.py`

#### "Bot ne répond pas"
- Vérifiez que le nom du bot dans `.env` correspond au nom utilisé dans le chat
- Testez les mentions : `@nom_du_bot hello`

#### "Gestionnaire ne fonctionne pas"
```bash
# Vérifiez les permissions
chmod +x bot_manager.sh

# Lancez avec debug
bash -x bot_manager.sh
```

### Logs et Debug

```bash
# Lancer avec plus de logs
LOG_LEVEL=DEBUG python3 bot.py

# Vérifier les logs en temps réel
tail -f logs/bot.log

# Avec le gestionnaire
./bot_manager.sh # Option 5: Voir les logs
```

## 📝 Fonctionnement en Background

### Avec le Gestionnaire (Recommandé)

```bash
./bot_manager.sh
# Sélectionnez "1. ▶️ Démarrer le bot"
```

### Méthodes Alternatives

```bash
# Avec nohup
nohup python3 bot.py > logs/bot.log 2>&1 &

# Avec screen
screen -S twitchbot
python3 bot.py
# Ctrl+A puis D pour détacher

# Avec systemd (pour démarrage auto)
sudo systemctl enable twitchbot.service
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Pushez sur votre branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🎉 Fonctionnalités à Venir

- [ ] Commandes de modération
- [ ] Intégration avec l'API Twitch complète
- [ ] Dashboard web de configuration
- [ ] Base de données pour historique
- [ ] Système de points/récompenses
- [ ] Mini-jeux dans le chat
- [ ] Interface web pour le gestionnaire
- [ ] API REST pour contrôle distant
- [ ] Système de plugins
- [ ] Backup et restauration automatique

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/bikininjas/twitch_ai_bot/issues)
- **Discussions** : [GitHub Discussions](https://github.com/bikininjas/twitch_ai_bot/discussions)
- **Documentation** : [BOT_MANAGER_README.md](BOT_MANAGER_README.md)

---

🤖 **Bot créé avec ❤️ et beaucoup de sarcasme pour la communauté Twitch !**

**Commandes rapides :**
- `./install.sh` - Installation automatique
- `./bot_manager.sh` - Gestionnaire interactif
- `./bot_manager.sh --help` - Aide sur les options CLI