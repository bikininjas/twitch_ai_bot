# 🤖 Twitch AI Bot

Un bot Twitch intelligent et sarcastique alimenté par Google Gemini AI qui interagit avec les utilisateurs dans le chat de votre chaîne.

## 🎯 Fonctionnalités

- **🤖 IA Sarcastique** : Réponses générées par Google Gemini avec une personnalité humoristique et sarcastique
- **🎮 Intégration Twitch** : Connexion IRC complète avec votre chaîne Twitch
- **👑 Interaction Privilégiée** : Répond automatiquement aux messages du propriétaire (`redpikpik`)
- **📢 Détection de Mentions** : Répond quand il est mentionné par d'autres utilisateurs
- **🎪 Jeux de Mots** : Créé des jeux de mots avec les pseudos des utilisateurs
- **⚡ Architecture Modulaire** : Code organisé par fonctionnalités dans des dossiers séparés

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
├── .env                        # Variables d'environnement (à configurer)
├── .gitignore                  # Fichiers ignorés par Git
├── requirements.txt            # Dépendances Python
├── bot.py                      # Script de lancement simple
└── README.md                   # Cette documentation
```

## 🚀 Installation

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

### 3. Installer les dépendances

```bash
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

Modifiez le fichier `.env` à la racine du projet :

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
```

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

### Lancement du Bot

```bash
# Méthode simple
python3 bot.py

# Ou directement
python3 src/main.py
```

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

## 🛠️ Configuration Avancée

### Logging

Ajoutez ces variables à votre `.env` pour personnaliser les logs :

```env
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
LOG_FILE=bot.log           # Fichier de log optionnel
```

### Personnalisation de la Personnalité

Modifiez les prompts dans `src/gemini_ai/response_generator.py` pour changer le style du bot.

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

### Logs et Debug

```bash
# Lancer avec plus de logs
LOG_LEVEL=DEBUG python3 bot.py

# Vérifier les logs en temps réel
tail -f bot.log
```

## 📝 Fonctionnement en Background

Pour faire tourner le bot en permanence sur WSL :

```bash
# Avec nohup
nohup python3 bot.py > bot.log 2>&1 &

# Avec screen
screen -S twitchbot
python3 bot.py
# Ctrl+A puis D pour détacher

# Avec systemd (recommandé)
# Créez un service systemd pour un démarrage automatique
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

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/bikininjas/twitch_ai_bot/issues)
- **Discussions** : [GitHub Discussions](https://github.com/bikininjas/twitch_ai_bot/discussions)

---

🤖 **Bot créé avec ❤️ et beaucoup de sarcasme pour la communauté Twitch !**