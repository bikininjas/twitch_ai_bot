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

# Configuration d'environnement
VENV_DIR=".venv"
PYTHON_BIN=""
PIP_BIN=""
PYTHON_ENV_BIN=""

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
        PYTHON_BIN=$(command -v python3)
        PYTHON_VERSION=$($PYTHON_BIN --version 2>&1 | cut -d' ' -f2)
        print_success "Python 3 détecté (version $PYTHON_VERSION)"
        return 0
    else
        print_error "Python 3 n'est pas installé"
        print_info "Veuillez installer Python 3.8+ avant de continuer"
        return 1
    fi
}

create_virtualenv() {
    print_step "Création de l'environnement virtuel (.venv)"

    if [ -d "$VENV_DIR" ]; then
        print_info "Environnement virtuel déjà présent dans $VENV_DIR"
    else
        if "$PYTHON_BIN" -m venv "$VENV_DIR"; then
            print_success "Environnement virtuel créé"
        else
            print_error "Échec de la création de l'environnement virtuel"
            return 1
        fi
    fi

    PIP_BIN="$VENV_DIR/bin/pip"
    PYTHON_ENV_BIN="$VENV_DIR/bin/python"

    if [ ! -x "$PYTHON_ENV_BIN" ]; then
        print_error "Python virtuel introuvable dans $VENV_DIR/bin/python"
        return 1
    fi

    return 0
}

# Installation des dépendances
install_dependencies() {
    print_step "Installation des dépendances Python"
    
    if [ -z "$PIP_BIN" ]; then
        PIP_BIN="$VENV_DIR/bin/pip"
    fi

    if [ ! -x "$PIP_BIN" ]; then
        print_error "pip introuvable dans l'environnement virtuel ($PIP_BIN)"
        return 1
    fi

    if [ -f "requirements.txt" ]; then
        if "$PIP_BIN" install -r requirements.txt; then
            print_success "Dépendances installées avec succès dans $VENV_DIR"
        else
            print_error "Échec de l'installation des dépendances"
            return 1
        fi
    else
        print_warning "Fichier requirements.txt non trouvé"
    fi

    return 0
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
    
    if [ -f ".env" ]; then
        print_info "Fichier .env existant détecté"
    elif [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Fichier .env créé à partir de .env.example"
        print_warning "Mettez à jour .env avec vos identifiants Twitch et Gemini"
    else
        print_warning "Modèle .env.example introuvable. Créez un fichier .env manuellement."
    fi
}

# Test de la configuration
test_configuration() {
    print_step "Test de la configuration"
    
    # Vérifier que le module principal peut être importé
    local python_bin=${PYTHON_ENV_BIN:-$PYTHON_BIN}

    if "$python_bin" -c "import src.main" 2>/dev/null; then
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

    if ! create_virtualenv; then
        exit 1
    fi
    
    create_directories
    setup_environment
    if ! install_dependencies; then
        exit 1
    fi
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
    echo -e "  ${YELLOW}1.${NC} Activez l'environnement virtuel: ${WHITE}source ${VENV_DIR}/bin/activate${NC}"
    echo -e "  ${YELLOW}2.${NC} Éditez le fichier ${WHITE}.env${NC} avec vos tokens et clés API"
    echo -e "  ${YELLOW}3.${NC} Lancez ${WHITE}./bot_manager.sh${NC} ou ${WHITE}nova${NC} (si alias configuré)"
    echo -e "  ${YELLOW}4.${NC} Utilisez le menu interactif pour gérer votre bot"
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