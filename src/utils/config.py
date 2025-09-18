"""
Configuration et logging pour le bot Twitch
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

def setup_logging(log_level: str = "DEBUG", log_dir: str = None) -> logging.Logger:
    """
    Configure le système de logging avec rotation
    
    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR)
        log_dir: Dossier des logs
        
    Returns:
        logging.Logger: Logger configuré
    """
    # Configuration du format de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Conversion du niveau de log
    numeric_level = getattr(logging, log_level.upper(), logging.DEBUG)
    
    # Créer le dossier de logs si nécessaire
    if not log_dir:
        log_dir = Path(__file__).parent.parent.parent / "logs"
    else:
        log_dir = Path(log_dir)
    
    log_dir.mkdir(exist_ok=True)
    
    # Fichier de log avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"bot_{timestamp}.log"
    
    # Configuration de base
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # Handler pour la console
            logging.StreamHandler(),
            # Handler pour fichier avec rotation
            RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,  # Garder 5 fichiers
                encoding='utf-8'
            )
        ]
    )
    
    # Logger principal
    logger = logging.getLogger("TwitchBot")
    logger.setLevel(numeric_level)
    
    # Nettoyer les anciens logs (garder seulement les 5 derniers)
    _cleanup_old_logs(log_dir)
    
    logger.info(f"Logging configuré - Niveau: {log_level}, Fichier: {log_file}")
    
    return logger

def _cleanup_old_logs(log_dir: Path, keep_count: int = 5):
    """
    Nettoie les anciens fichiers de log
    
    Args:
        log_dir: Dossier des logs
        keep_count: Nombre de fichiers à garder
    """
    try:
        # Récupérer tous les fichiers de log
        log_files = list(log_dir.glob("bot_*.log*"))
        
        # Trier par date de modification (plus récent en premier)
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Supprimer les fichiers en trop
        for old_log in log_files[keep_count:]:
            try:
                old_log.unlink()
                print(f"Ancien log supprimé: {old_log.name}")
            except Exception as e:
                print(f"Erreur lors de la suppression de {old_log}: {e}")
                
    except Exception as e:
        print(f"Erreur lors du nettoyage des logs: {e}")

def load_config() -> dict:
    """
    Charge la configuration depuis les variables d'environnement
    
    Returns:
        dict: Configuration du bot
    """
    load_dotenv()
    
    config = {
        # Twitch
        "twitch": {
            "bot_token": os.getenv("TWITCH_BOT_TOKEN"),
            "client_id": os.getenv("TWITCH_BOT_CLIENT_ID"),
            "channel": os.getenv("TWITCH_CHANNEL"),
            "bot_name": os.getenv("TWITCH_BOT_NAME")
        },
        
        # Gemini AI
        "gemini": {
            "api_key": os.getenv("GEMINI_API_KEY")
        },
        
        # Comportement du bot
        "behavior": {
            "owner_username": os.getenv("OWNER_USERNAME", "redpikpik"),
            "personality": os.getenv("BOT_PERSONALITY", "sarcastic")
        },
        
        # Logging
        "logging": {
            "level": os.getenv("LOG_LEVEL", "DEBUG"),
            "dir": os.getenv("LOG_DIR", "logs")
        }
    }
    
    return config

def validate_config(config: dict) -> bool:
    """
    Valide la configuration
    
    Args:
        config: Configuration à valider
        
    Returns:
        bool: True si la configuration est valide
    """
    required_fields = [
        ("twitch", "bot_token"),
        ("twitch", "client_id"),
        ("twitch", "channel"),
        ("twitch", "bot_name"),
        ("gemini", "api_key")
    ]
    
    for section, field in required_fields:
        if not config.get(section, {}).get(field):
            return False
    
    return True

def get_startup_message() -> str:
    """
    Retourne le message de démarrage du bot
    
    Returns:
        str: Message de démarrage
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
╔══════════════════════════════════════╗
║           TWITCH AI BOT              ║
║        Démarrage - {timestamp}        ║
╚══════════════════════════════════════╝

🤖 Bot sarcastique alimenté par Gemini AI
🎮 Prêt à trolller le chat de redpikpik
💬 En attente de mentions et messages...
🗂️  Logs sauvegardés dans le dossier logs/
"""