"""
Logging configuration for the application.
"""
import logging
import logging.config
import json
import sys
from app.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(timestamp)s %(level)s %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.LOG_LEVEL,
            "formatter": settings.LOG_FORMAT,
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": settings.LOG_LEVEL,
            "formatter": settings.LOG_FORMAT,
            "filename": "logs/app.log",
            "maxBytes": 10485760,
            "backupCount": 5
        }
    },
    "root": {
        "level": settings.LOG_LEVEL,
        "handlers": ["console"] if settings.LOG_OUTPUT in ["console", "both"] else []
    }
}

if settings.LOG_OUTPUT in ["file", "both"]:
    LOGGING_CONFIG["root"]["handlers"].append("file")

def setup_logging():
    """Configure logging for the application."""
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(__name__)

logger = setup_logging()
