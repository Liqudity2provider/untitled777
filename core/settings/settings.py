"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from datetime import timedelta

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h6__pz5m$yk#s2l93$c6ux=%!r1hm%3h%5-^$pb9wzv5^gp*@3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.herokuapp.com', '127.0.0.1']
MY_URLS = ['http://127.0.0.1:8000/', 'http://django-chat-test5050.herokuapp.com/']
ACTIVE_URL = 1
# Application definition

INSTALLED_APPS = [
    'chat',
    'channels',
    'django.contrib.sites',

    'users.apps.UsersConfig',
    'blog.apps.BlogConfig',
    'crispy_forms',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'films',
    'mptt',

    # rest-social-auth
    'social_django',
    'rest_framework.authtoken',
    'rest_social_auth',
    'rest_framework_swagger',
    # roles in admin page
    'rolepermissions',

    # to store files in DropBox
    'django_dropbox_storage',

]
# DropBox
DEFAULT_FILE_STORAGE = 'django_dropbox_storage.storage.DropboxStorage'
DROPBOX_ACCESS_TOKEN = 'K8Oox5d-iMwAAAAAAAAAAS0VdDVcD7DdqLwPAhaU9lW-d4EhfROw5jVQCUqQUBXa'

X_FRAME_OPTIONS = 'SAMEORIGIN'  # (django admin page interface) only if django version >= 3.0

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
ROOT_URLCONF = 'core.urls'

SITE_ID = 2

TEMPLATES = [
    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            # for swagger
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'users.context_processors.social_app_keys',
                'django_settings_export.settings_export',

            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = os.path.join(BASE_DIR, "static/")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'
PTH_TO_REDIRECT = '../profile'

SETTINGS_EXPORT = [
    'PTH_TO_REDIRECT',
]
ASGI_APPLICATION = "core.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SOCIAL_AUTH_FACEBOOK_KEY = '295137440610143'
SOCIAL_AUTH_FACEBOOK_SECRET = '4b4aef291799a7b9aaf016689339e97f'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': ','.join([
        # public_profile
        'id', 'cover', 'name', 'first_name', 'last_name', 'age_range', 'link',
        'gender', 'locale', 'picture', 'timezone', 'updated_time', 'verified',
        # extra fields
        'email',
    ]),
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    '132715411999-k6s2b050id792h6o0lft3db2str3buka.apps.googleusercontent.com'
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '4g9DyldJeb0FEfrxxeJow1DF'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', ]

SOCIAL_AUTH_TWITTER_KEY = 'gCrpEpNxpWkAE6Cul98OzAWTk'
SOCIAL_AUTH_TWITTER_SECRET = '7SYSRpYY4amW5kiNXUAxUDdWS7G3nHytRIGHbDVTByzBfsqDJl'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',  # OAuth1.0
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'users.social_pipeline.auto_logout',  # custom action
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'users.social_pipeline.check_for_email',  # custom action
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'users.social_pipeline.save_avatar',  # custom action
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'rest_social_auth': {
            'handlers': ['console', ],
            'level': "DEBUG",
        },
    }
}

REST_FRAMEWORK = {
    # for swagger
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
REST_SESSION_LOGIN = False
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-access-token'  # you can set these
JWT_AUTH_REFRESH_COOKIE = 'jwt-refresh-token'  # to anything
JWT_AUTH_SECURE = True
CORS_ALLOW_CREDENTIALS = True

ROLEPERMISSIONS_MODULE = 'core.roles'

FIREBASE_CONFIG = {
    'apiKey': "AIzaSyC_S0lPqRUwsbNJ0x-i-kv8RrHd5Coyqw8",
    'authDomain': "memories-9ec47.firebaseapp.com",
    'projectId': "memories-9ec47",
    'serviceAccount': 'serviceAccountKeyFirebase.json',
    'databaseURL': 'gs://memories-9ec47.appspot.com',
    'storageBucket': "memories-9ec47.appspot.com",
    # 'messagingSenderId': "132715411999",
    # 'appId': "1:132715411999:web:1655dc229486eab8ba732a"
}


