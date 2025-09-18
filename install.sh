#!/bin/bash

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                        🚀 NOVA BOT INSTALLER 🚀                             ║
# ║                    Installation automatique du bot                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Émojis
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="ℹ️"
GEAR="⚙️"

print_header() {
    clear
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${WHITE}                        ${ROCKET} NOVA BOT INSTALLER ${ROCKET}                             ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${CYAN}                    Installation automatique du bot                          ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}${GEAR} $1...${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARNING} $1${NC}"
}

print_info() {
    echo -e "${CYAN}${INFO} $1${NC}"
}

# Vérification de Python
check_python() {
    print_step "Vérification de Python"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python 3 détecté (version $PYTHON_VERSION)"
        return 0
    else
        print_error "Python 3 n'est pas installé"
        print_info "Veuillez installer Python 3.8+ avant de continuer"
        return 1
    fi
}

# Installation des dépendances
install_dependencies() {
    print_step "Installation des dépendances Python"
    
    if [ -f "requirements.txt" ]; then
        if python3 -m pip install -r requirements.txt; then
            print_success "Dépendances installées avec succès"
        else
            print_error "Échec de l'installation des dépendances"
            return 1
        fi
    else
        print_warning "Fichier requirements.txt non trouvé"
    fi
}

# Création de la structure de dossiers
create_directories() {
    print_step "Création de la structure de dossiers"
    
    mkdir -p logs
    mkdir -p config
    
    print_success "Dossiers créés"
}

# Configuration des variables d'environnement
setup_environment() {
    print_step "Configuration de l'environnement"
    
    # Créer un fichier .env d'exemple s'il n'existe pas
    if [ ! -f ".env" ]; then
        cat > .env << 'EOF'
# Configuration Nova Bot
# Copiez ce fichier et remplissez vos valeurs

# Twitch Configuration
TWITCH_BOT_TOKEN=your_twitch_oauth_token_here
TWITCH_CHANNEL=your_channel_name_here
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
EOF
        print_success "Fichier .env d'exemple créé"
        print_warning "Veuillez éditer le fichier .env avec vos vraies valeurs"
    else
        print_info "Fichier .env existant détecté"
    fi
}

# Test de la configuration
test_configuration() {
    print_step "Test de la configuration"
    
    # Vérifier que le module principal peut être importé
    if python3 -c "import src.main" 2>/dev/null; then
        print_success "Module principal importable"
    else
        print_warning "Impossible d'importer le module principal (vérifiez .env)"
    fi
}

# Configuration des alias et raccourcis
setup_shortcuts() {
    print_step "Configuration des raccourcis"
    
    # Créer un alias dans le .bashrc de l'utilisateur si souhaité
    echo ""
    echo -e "${YELLOW}Voulez-vous ajouter un alias 'nova' pour démarrer le gestionnaire? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        ALIAS_LINE="alias nova='$(pwd)/bot_manager.sh'"
        
        # Ajouter à .bashrc s'il n'y est pas déjà
        if ! grep -q "alias nova=" ~/.bashrc 2>/dev/null; then
            echo "" >> ~/.bashrc
            echo "# Nova Bot Manager Alias" >> ~/.bashrc
            echo "$ALIAS_LINE" >> ~/.bashrc
            print_success "Alias 'nova' ajouté à ~/.bashrc"
            print_info "Exécutez 'source ~/.bashrc' ou redémarrez votre terminal"
        else
            print_info "Alias 'nova' déjà présent dans ~/.bashrc"
        fi
    fi
}

# Fonction principale d'installation
main() {
    print_header
    
    echo -e "${CYAN}Cette installation va configurer Nova Bot Manager${NC}"
    echo -e "${CYAN}Appuyez sur Entrée pour continuer ou Ctrl+C pour annuler${NC}"
    read -r
    
    print_header
    
    # Étapes d'installation
    if ! check_python; then
        exit 1
    fi
    
    create_directories
    setup_environment
    install_dependencies
    test_configuration
    setup_shortcuts
    
    # Fin d'installation
    print_header
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${WHITE}                          INSTALLATION TERMINÉE                              ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    print_success "Nova Bot Manager installé avec succès!"
    echo ""
    print_info "Prochaines étapes:"
    echo -e "  ${YELLOW}1.${NC} Éditez le fichier ${WHITE}.env${NC} avec vos tokens et clés API"
    echo -e "  ${YELLOW}2.${NC} Lancez ${WHITE}./bot_manager.sh${NC} ou ${WHITE}nova${NC} (si alias configuré)"
    echo -e "  ${YELLOW}3.${NC} Utilisez le menu interactif pour gérer votre bot"
    echo ""
    print_info "Fichiers importants:"
    echo -e "  ${CYAN}Configuration:${NC} .env"
    echo -e "  ${CYAN}Gestionnaire:${NC} ./bot_manager.sh"
    echo -e "  ${CYAN}Logs:${NC} logs/nova_bot.log"
    echo ""
    echo -e "${BLUE}Documentation: https://github.com/bikininjas/twitch_ai_bot${NC}"
    echo ""
    
    echo -e "${YELLOW}Voulez-vous lancer le gestionnaire maintenant? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        ./bot_manager.sh
    fi
}

# Point d'entrée
main "$@"