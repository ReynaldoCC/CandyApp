from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True

SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="ZAWuI0O2l5DGz6803JHdRGpFzesgdyjGquqHEdSDgWnt7WIJDEvmi7vFM4UAlc99",
)
ALLOWED_HOSTS = ["*"]

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# django-debug-toolbar
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2", "172.20.25.62"]

# Celery
# ------------------------------------------------------------------------------
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Your stuff...
# ------------------------------------------------------------------------------
