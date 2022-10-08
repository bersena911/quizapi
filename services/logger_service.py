import logging.config

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {"format": "%(asctime)s [%(process)s] %(levelname)s: %(message)s"}
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "INFO",
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "gunicorn": {"propagate": True},
        "gunicorn.access": {"propagate": True},
        "gunicorn.error": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "uvicorn.error": {"propagate": True},
    },
}


def set_log_configuration():
    """
    Creates logging configuration
    """
    logging.config.dictConfig(LOG_CONFIG)
