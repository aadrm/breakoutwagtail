from django.conf import settings

FORMATTERS = (
    {
        "verbose": {
            "format": "{levelname} {asctime:s} {threadName} {thread:d} {module} {filename} {lineno:d} {name} {funcName} {process:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime:s} {module} {filename} {lineno:d} {funcName} {message}",
            "style": "{",
        },
    },
)

HANDLERS = {
    "console_handler": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
    "default_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "logs/breakout.log",
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "simple",
        "backupCount": 3,
        "maxBytes": 1024 * 1024 * 3,
    },
    "detailed_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "logs/breakout-detail.log",
        "mode": "a",
        "formatter": "verbose",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 3,
    },
}

LOGGERS = (
    {
        "django": {
            "handlers": ["console_handler", "detailed_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["my_handler"],
            "level": "WARNING",
            "propagate": False,
        },
    },
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS[0],
}
