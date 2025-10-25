#!/bin/bash

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                          🤖 NOVA BOT MANAGER 🤖                              ║
# ║              Script de gestion pour nova_the_red_cat Twitch Bot             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# Configuration
BOT_NAME="nova_the_red_cat"
VENV_DIR=".venv"
PYTHON_BIN="$VENV_DIR/bin/python"
BOT_SCRIPT="$PYTHON_BIN -m src.main"
PID_FILE="logs/bot.pid"
LOG_DIR="$PWD/logs"

# Fonction pour obtenir le dernier fichier de log
get_latest_log_file() {
    local latest_log=$(ls -t "$LOG_DIR"/bot_*.log 2>/dev/null | head -1)
    if [ -n "$latest_log" ]; then
        echo "$latest_log"
    else
        echo "$LOG_DIR/nova_bot.log"
    fi
}

LOG_FILE=$(get_latest_log_file)

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Émojis
ROBOT="🤖"
FIRE="🔥"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="ℹ️"
ROCKET="🚀"
STOP="🛑"
RELOAD="🔄"

# Créer le dossier logs s'il n'existe pas
mkdir -p "$LOG_DIR"

# Fonction pour afficher le header
print_header() {
    clear
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${WHITE}                          ${ROBOT} NOVA BOT MANAGER ${ROBOT}                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${CYAN}              Script de gestion pour nova_the_red_cat Twitch Bot             ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Fonction pour vérifier si le bot est en cours d'exécution
is_bot_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # Running
        else
            rm -f "$PID_FILE"
            return 1  # Not running
        fi
    else
        return 1  # Not running
    fi
}

# Fonction pour obtenir le PID du bot
get_bot_pid() {
    if [ -f "$PID_FILE" ]; then
        cat "$PID_FILE"
    else
        echo "N/A"
    fi
}

# Fonction pour afficher le statut du bot
show_status() {
    print_header
    
    if is_bot_running; then
        local pid=$(get_bot_pid)
        local uptime=$(ps -o etime= -p "$pid" 2>/dev/null | tr -d ' ')
        echo -e "${GREEN}${CHECK} Status: ${BOT_NAME} est ${GREEN}EN COURS D'EXÉCUTION${NC}"
        echo -e "${BLUE}${INFO} PID: ${WHITE}$pid${NC}"
        echo -e "${BLUE}${INFO} Uptime: ${WHITE}$uptime${NC}"
        echo -e "${BLUE}${INFO} Log file: ${WHITE}$LOG_FILE${NC}"
    else
        echo -e "${RED}${CROSS} Status: ${BOT_NAME} est ${RED}ARRÊTÉ${NC}"
    fi
    echo ""
}

# Fonction pour démarrer le bot
start_bot() {
    print_header
    
    if is_bot_running; then
        echo -e "${YELLOW}${WARNING} Le bot est déjà en cours d'exécution (PID: $(get_bot_pid))${NC}"
        return 1
    fi

    if [ ! -x "$PYTHON_BIN" ]; then
        echo -e "${RED}${CROSS} Environnement virtuel introuvable (${PYTHON_BIN})${NC}"
        echo -e "${YELLOW}${WARNING} Créez-le avec: python3 -m venv ${VENV_DIR}${NC}"
        echo -e "${YELLOW}${WARNING} Puis installez les dépendances avec: source ${VENV_DIR}/bin/activate && pip install -r requirements.txt${NC}"
        return 1
    fi
    
    echo -e "${BLUE}${ROCKET} Démarrage de ${BOT_NAME}...${NC}"
    
    # Démarrer le bot en arrière-plan (le bot Python gère ses propres logs horodatés)
    nohup $BOT_SCRIPT > /dev/null 2>&1 &
    local pid=$!
    
    # Sauvegarder le PID
    echo "$pid" > "$PID_FILE"
    
    # Attendre un peu pour vérifier que le démarrage s'est bien passé
    sleep 3
    
    # Mettre à jour la référence au fichier de log après démarrage
    LOG_FILE=$(get_latest_log_file)
    
    if is_bot_running; then
        echo -e "${GREEN}${CHECK} ${BOT_NAME} démarré avec succès (PID: $pid)${NC}"
        echo -e "${BLUE}${INFO} Logs: tail -f $LOG_FILE${NC}"
        echo -e "${CYAN}${INFO} Fichier de log: $(basename "$LOG_FILE")${NC}"
    else
        echo -e "${RED}${CROSS} Échec du démarrage du bot${NC}"
        echo -e "${YELLOW}${WARNING} Vérifiez les logs: ls -la $LOG_DIR/bot_*.log${NC}"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Fonction pour arrêter le bot
stop_bot() {
    print_header
    
    if ! is_bot_running; then
        echo -e "${YELLOW}${WARNING} Le bot n'est pas en cours d'exécution${NC}"
        return 1
    fi
    
    local pid=$(get_bot_pid)
    echo -e "${YELLOW}${STOP} Arrêt de ${BOT_NAME} (PID: $pid)...${NC}"
    
    # Tentative d'arrêt propre
    kill "$pid" 2>/dev/null
    
    # Attendre jusqu'à 10 secondes pour l'arrêt propre
    local count=0
    while [ $count -lt 10 ] && is_bot_running; do
        sleep 1
        count=$((count + 1))
    done
    
    if is_bot_running; then
        echo -e "${YELLOW}${WARNING} Arrêt forcé...${NC}"
        kill -9 "$pid" 2>/dev/null
        sleep 1
    fi
    
    rm -f "$PID_FILE"
    
    if ! is_bot_running; then
        echo -e "${GREEN}${CHECK} ${BOT_NAME} arrêté avec succès${NC}"
        echo "=== BOT STOPPED - $(date) ===" >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"
    else
        echo -e "${RED}${CROSS} Échec de l'arrêt du bot${NC}"
        return 1
    fi
}

# Fonction pour redémarrer le bot
restart_bot() {
    print_header
    echo -e "${BLUE}${RELOAD} Redémarrage de ${BOT_NAME}...${NC}"
    echo ""
    
    if is_bot_running; then
        stop_bot
        sleep 2
    fi
    
    start_bot
}

# Fonction pour afficher les logs en temps réel
show_logs() {
    print_header
    
    # Mettre à jour la référence au fichier de log
    LOG_FILE=$(get_latest_log_file)
    
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}${WARNING} Aucun fichier de log trouvé dans $LOG_DIR${NC}"
        echo -e "${BLUE}${INFO} Fichiers disponibles:${NC}"
        ls -la "$LOG_DIR"/bot_*.log 2>/dev/null || echo -e "${RED}${CROSS} Aucun fichier de log bot_*.log trouvé${NC}"
        return 1
    fi
    
    echo -e "${BLUE}${INFO} Affichage des logs en temps réel (Ctrl+C pour quitter)${NC}"
    echo -e "${BLUE}${INFO} Fichier: $(basename "$LOG_FILE")${NC}"
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${WHITE}                                LOGS EN TEMPS RÉEL                             ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    tail -f "$LOG_FILE"
}

# Fonction pour afficher les dernières lignes de log
show_recent_logs() {
    print_header
    
    # Mettre à jour la référence au fichier de log
    LOG_FILE=$(get_latest_log_file)
    
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}${WARNING} Aucun fichier de log trouvé dans $LOG_DIR${NC}"
        echo -e "${BLUE}${INFO} Fichiers disponibles:${NC}"
        ls -la "$LOG_DIR"/bot_*.log 2>/dev/null || echo -e "${RED}${CROSS} Aucun fichier de log bot_*.log trouvé${NC}"
        return 1
    fi
    
    echo -e "${BLUE}${INFO} Dernières 50 lignes du log: $(basename "$LOG_FILE")${NC}"
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${WHITE}                               LOGS RÉCENTS                                   ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    tail -n 50 "$LOG_FILE" 2>/dev/null || echo -e "${RED}${CROSS} Impossible de lire le fichier de log${NC}"
}

# Fonction pour le menu interactif
show_menu() {
    while true; do
        show_status
        
        echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${CYAN}║${WHITE}                                   MENU                                       ${CYAN}║${NC}"
        echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${WHITE}1.${NC} ${GREEN}${ROCKET} Démarrer le bot${NC}"
        echo -e "${WHITE}2.${NC} ${RED}${STOP} Arrêter le bot${NC}"
        echo -e "${WHITE}3.${NC} ${YELLOW}${RELOAD} Redémarrer le bot${NC}"
        echo -e "${WHITE}4.${NC} ${BLUE}${INFO} Voir les logs en temps réel${NC}"
        echo -e "${WHITE}5.${NC} ${PURPLE}${INFO} Voir les logs récents${NC}"
        echo -e "${WHITE}6.${NC} ${CYAN}${RELOAD} Actualiser le statut${NC}"
        echo -e "${WHITE}0.${NC} ${WHITE}${CROSS} Quitter${NC}"
        echo ""
        echo -ne "${YELLOW}Votre choix: ${NC}"
        
        read -r choice
        
        case $choice in
            1)
                start_bot
                echo ""
                echo -ne "${YELLOW}Appuyez sur Entrée pour continuer...${NC}"
                read -r
                ;;
            2)
                stop_bot
                echo ""
                echo -ne "${YELLOW}Appuyez sur Entrée pour continuer...${NC}"
                read -r
                ;;
            3)
                restart_bot
                echo ""
                echo -ne "${YELLOW}Appuyez sur Entrée pour continuer...${NC}"
                read -r
                ;;
            4)
                show_logs
                ;;
            5)
                show_recent_logs
                echo ""
                echo -ne "${YELLOW}Appuyez sur Entrée pour continuer...${NC}"
                read -r
                ;;
            6)
                # Juste continuer la boucle pour actualiser
                ;;
            0)
                print_header
                echo -e "${GREEN}${CHECK} Merci d'avoir utilisé Nova Bot Manager!${NC}"
                echo -e "${BLUE}${INFO} Pour plus d'infos: github.com/bikininjas/twitch_ai_bot${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo -e "${RED}${CROSS} Choix invalide!${NC}"
                sleep 1
                ;;
        esac
    done
}

# Fonction d'aide
show_help() {
    print_header
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${WHITE}                                   AIDE                                        ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${WHITE}Usage: $0 [COMMANDE]${NC}"
    echo ""
    echo -e "${YELLOW}Commandes disponibles:${NC}"
    echo -e "  ${GREEN}start${NC}     - Démarrer le bot en arrière-plan"
    echo -e "  ${RED}stop${NC}      - Arrêter le bot"
    echo -e "  ${YELLOW}restart${NC}   - Redémarrer le bot"
    echo -e "  ${BLUE}status${NC}    - Afficher le statut du bot"
    echo -e "  ${PURPLE}logs${NC}      - Afficher les logs en temps réel"
    echo -e "  ${PURPLE}recent${NC}    - Afficher les logs récents"
    echo -e "  ${CYAN}menu${NC}      - Mode interactif (par défaut)"
    echo -e "  ${WHITE}help${NC}      - Afficher cette aide"
    echo ""
    echo -e "${BLUE}${INFO} Fichiers:${NC}"
    echo -e "  PID: ${WHITE}$PID_FILE${NC}"
    echo -e "  Logs: ${WHITE}$LOG_FILE${NC}"
    echo ""
}

# Traitement des arguments de ligne de commande
case "${1:-menu}" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    recent)
        show_recent_logs
        ;;
    menu)
        show_menu
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}${CROSS} Commande inconnue: $1${NC}"
        echo -e "${YELLOW}${INFO} Utilisez '$0 help' pour voir l'aide${NC}"
        exit 1
        ;;
esac