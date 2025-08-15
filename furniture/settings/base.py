from pathlib import Path
import environ
from datetime import timedelta


env = environ.Env(

    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent


environ.Env.read_env(BASE_DIR / '.env')


SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []




INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    'store.apps.StoreConfig',
    'blog.apps.BlogConfig',
    'cart.apps.CartConfig',
    'wishlist.apps.WishlistConfig',
    'users.apps.UsersConfig',
    'orders.apps.OrdersConfig',
    'api.apps.ApiConfig',
    'comparison.apps.ComparisonConfig',


    'django_cleanup.apps.CleanupConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_spectacular',
    'imagekit',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'furniture.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.categories',
                'cart.context_processors.cart',
                'wishlist.context_processors.wishlist',
                'comparison.context_processors.comparison',
                'store.context_processors.special_offer',
            ],
            'libraries': {
                'blog_tags': 'blog.templatetags.blog_tags',
                'store_tags': 'store.templatetags.store_tags',
                'comparison_tags': 'comparison.templatetags.comparison_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'furniture.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]



LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True



STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


STORAGES = {
    "default": {
        "BACKEND": "furniture.storage_backends.OverwriteStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}



FIXTURE_DIRS = [ BASE_DIR / 'fixtures', ]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CART_SESSION_ID = 'cart'
WISH_SESSION_ID = 'wishlist'
COMPARISON_SESSION_ID = 'comparison'
RECENTLY_VIEWED_SESSION_ID = 'recently_viewed'


LOGIN_REDIRECT_URL = 'store:account'
LOGOUT_REDIRECT_URL = 'store:home'
LOGIN_URL = 'users:login'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@domusaurea.com'


CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}



SPECTACULAR_SETTINGS = {
    'TITLE': 'Domus Aurea API',
    'DESCRIPTION': 'API для мебельного магазина Domus Aurea',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}



JAZZMIN_SETTINGS = {
    # --- Titles ---
    "site_title": "Domus Aurea Admin",
    "site_header": "Domus Aurea",
    "site_brand": "Domus Aurea",
    "welcome_sign": "Добро пожаловать в панель управления Domus Aurea",
    "copyright": "Domus Aurea Ltd.",

    # --- Logo (установлено в None, чтобы отображался только текст) ---
    "site_logo": None,
    "login_logo": None,

    # --- Theme ---
    "theme": "lux",

    # --- Top Menu ---
    "topmenu_links": [
        {"name": "Главная", "url": "admin:index"},
        {"name": "Перейти на сайт", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],

    # --- UI Tweaks ---
    "show_sidebar": True,
    "navigation_expanded": True,
    "related_modal_active": True,
    "language_chooser": False,
    "ui_tweaks": {
       "navbar": "navbar-dark",
       "sidebar": "sidebar-dark-primary",
       "theme": "lux",
       "sidebar_nav_flat_style": True,
    }
}


# --- CKEDITOR CONFIGURATION ---
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 400,
        'width': '100%',
        'toolbar_Custom': [
            ['Source', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['Find', 'Replace', '-', 'SelectAll'],
            '/',
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            '/',
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize'],
        ],
        # Добавляем наши кастомные стили
        'stylesSet': [
            {
                'name': 'Информационный блок',
                'element': 'div',
                'attributes': {'class': 'info-box'},
            },
            {
                'name': 'Оглавление (пунктир)',
                'element': 'div',
                'attributes': {'class': 'toc-dashed'},
            },
        ],
        'extraAllowedContent': 'h2[id]; h3[id]; h4[id]; div(toc-custom, info-box, toc-dashed);',
    },
}