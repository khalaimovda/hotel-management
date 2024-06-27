import os
from pathlib import Path

from dotenv import load_dotenv
from django.db.backends.postgresql.psycopg_any import IsolationLevel

load_dotenv()

CITY_FETCH_URL = os.getenv(key='CITY_FETCH_URL')
HOTEL_FETCH_URL = os.getenv(key='HOTEL_FETCH_URL')
FETCH_USERNAME = os.getenv(key='FETCH_USERNAME')
FETCH_PASSWORD = os.getenv(key='FETCH_PASSWORD')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(key='SECRET_KEY', default='django-insecure-)ce5dwh$rln*6#9^heucll7+(f^ms74_z%s@=@g365zj&qext!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', default='False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'hotel-management',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # libraries
    'django_crontab',

    # local apps
    'hotels.apps.HotelsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotel_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'hotel_management_system/templates',
        ],
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

WSGI_APPLICATION = 'hotel_management_system.wsgi.application'

# Pagination
ITEMS_PER_PAGE = 15

# Database
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

DB_HOST = os.getenv('DB_HOST')
DB_HOST = '127.0.0.1' if DB_HOST == 'localhost' else DB_HOST

DB_PORT = os.getenv('DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'isolation_level': IsolationLevel.READ_COMMITTED,
        },
    }
}


# CronJobs
CRONTAB_COMMAND_PREFIX = (  # "Needed to ensure environment variables are accessible in the cronjob
    f'CITY_FETCH_URL={CITY_FETCH_URL} '
    f'HOTEL_FETCH_URL={HOTEL_FETCH_URL} '
    f'FETCH_USERNAME={FETCH_USERNAME} '
    f'FETCH_PASSWORD={FETCH_PASSWORD} '
    
    f'DB_NAME={DB_NAME} '
    f'DB_USERNAME={DB_USERNAME} '
    f'DB_PASSWORD={DB_PASSWORD} '
    f'DB_HOST={DB_HOST} '
    f'DB_PORT={DB_PORT}'
)

CRONJOBS = [
    # Fetch city and hotel data every day
    (
        '0 0 * * *',  # '* * * * *' -- for execution every minute
        'hotels.jobs.fetch_hotel_data',
        [],
        {
            'city_url': CITY_FETCH_URL,
            'hotel_url': HOTEL_FETCH_URL,
            'username': FETCH_USERNAME,
            'password': FETCH_PASSWORD,
        }
    ),
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/logfile.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'hotels': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
