import logging
from logging.config import dictConfig

def logger_settings(service_name: str, log_level: str):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": f"[%(asctime)s] [%(levelname)s] /{service_name} %(name)s:%(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": log_level},
        },
    }

# Настройка логгера
log_settings = logger_settings("DICE_SERVICE", "INFO")
dictConfig(log_settings)
logger = logging.getLogger(__name__)