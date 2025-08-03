from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Django Debug Toolbar
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# IP-адреса, с которых будет виден debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# Настройки для отправки почты (вывод в консоль для отладки)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'