"""
Django settings for uo_core project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/DEBUG

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import environ
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-24(4eiik(4^i@o*01mermb79l*dy_u*ixfg7@2s2(1yzb$s)d3'

# SECURITY WARNING: don't run with debug turned on in production!
root = environ.Path(__file__) - 1
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

DEBUG = os.environ.get('DEBUG') == 'TRUE'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'drf_api_logger',
    'adminsortable2',
    'rest_framework',
    'parler',
    'ckeditor',
    'ckeditor_uploader',
    'django_user_agents',
    'django_paranoid',
    'django_filters',
    'drf_yasg',
    'corsheaders',
    'prettyjson',
    'django_json_widget',
    'admin_auto_filters',
    'django_admin_listfilter_dropdown',
    'multiselectfield',
    'storages',
    'rangefilter',
    'simple_history',

    'account.apps.AccountConfig',
    'sales.apps.SalesConfig',
    'surgalt.apps.SurgaltConfig',
    # 'account.social_auth.apps.SocialAuthConfig',
]

CKEDITOR_UPLOAD_PATH = 'uo_core_package_pics'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Smiley', 'CodeSnippet'],
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            ['TextColor', 'BGColor'],
            ['Link', 'Unlink'],
            ['NumberedList', 'BulletedList'],
            ['Maximize']
        ],
        'height': 150,
    },
}

# if DEBUG:
if True:

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_HEADERS = list(default_headers) + [
        'accept-language',
        'x-display-currency',
        'Accept-Language',
        'X-Display-Currency',
    ]
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        "https://tapatrip.com",
        "https://www.tapatrip.com",
    ]

""" JWT AND AUTH """
LOGIN_URL = '/admin/login/'

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "U0@code")
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "username",
    "USER_ID_CLAIM": "username",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


AUTH_USER_MODEL = 'account.UserModel'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'tapatrip_backend.middleware.NotificationTokenMiddleware',
    # 'tapatrip_backend.middleware.CurrencyAndLanguageMiddleware',
    # 'tapatrip_backend.middleware.StatsMiddleware',
    # 'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

X_FRAME_OPTIONS = "SAMEORIGIN"
ROOT_URLCONF = 'uo_core.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'uo_core.wsgi.application'

DATA_UPLOAD_MAX_MEMORY_SIZE = 10242880

TIME_ZONE = 'Asia/Ulaanbaatar'

DATETIME_FORMAT = 'Y-m-d H:i:s'
DATETIME = 'Y-m-d'

# mn_format.DATETIME_FORMAT = "Y-m-d H:i:s"
# mn_format.DATE_FORMAT = "Y-m-d"

USE_I18N = False
USE_L10N = False
DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = ' '
USE_THOUSAND_SEPARATOR = True

# PARLER_LANGUAGES = {
#     None: (
#         {'code': 'mn', },
#         {'code': 'en', },
#         {'code': 'zh', },
#     ),
#     'default': {
#         'fallbacks': ['mn'],
#         'hide_untranslated': False,  # Default
#     }
# }

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('USERNAME'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOSTNAME'),
        'PORT': os.environ.get('PORT'),
        'AUTOCOMMIT': True,
        'ATOMIC_REQUESTS': False,
        'TEST_MIRROR': None,
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static_files"),
    ]

FILE_UPLOAD_STORAGE = env("FILE_UPLOAD_STORAGE", default="local")  # local | s3

if FILE_UPLOAD_STORAGE == "local":
    MEDIA_ROOT_NAME = "media"
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"

if FILE_UPLOAD_STORAGE == "s3":
    # Using django-storages
    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_S3_ACCESS_KEY_ID = env("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = env("AWS_S3_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
    # AWS_S3_SIGNATURE_VERSION = env("AWS_S3_SIGNATURE_VERSION", default="s3v4")

    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL", default=None)
    AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (
        AWS_STORAGE_BUCKET_NAME,
        AWS_S3_REGION_NAME,
    )
    MEDIAFILES_LOCATION = "core/original/media"
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

    #
    # AWS_PRESIGNED_EXPIRY = env.int("AWS_PRESIGNED_EXPIRY", default=10)  # seconds

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter', ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'uo_core.custom_response_utils.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        # 'rest_framework_datatables.renderers.DatatablesRenderer',
        # 'drf_renderer_xlsx.renderers.XLSXRenderer',
    ),
    # PAGINATION
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 25,
    'EXCEPTION_HANDLER': 'uo_core.custom_response_utils.handle_exception',

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3000/day',
        'user': '10000/day'
    }
}

# LANGUAGE_CODE = 'en-us'

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "slack_admins": {
                "level": "ERROR",
                "class": "uo_core.slack_logger.SlackExceptionHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["slack_admins"],
                "level": "INFO",
            },
        },
    }
