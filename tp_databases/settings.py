import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'v2djqhjv=rpc#tcayfc4*snav#dff-p44ni&zaj=7(vnu=qrb4'

DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'rest_framework',

    'user',
    'forum',
    'utils',
]

# Response codes

RESPONSE_CODE_OK = 0
RESPONSE_CODE_OBJECT_NOT_FOUND = 1
RESPONSE_CODE_NOT_VALID = 2
RESPONSE_CODE_INVALID_REQUEST = 3
RESPONSE_CODE_UNEXPECTED_ERROR = 4
RESPONSE_CODE_USER_ALREADY_EXISTS = 5

RESPONSE_MSG_OBJECT_NOT_FOUND = 'Object not found'
RESPONSE_MSG_NOT_VALID = 'Data is invalid'
RESPONSE_MSG_INVALID_REQUEST = 'Request is invalid'
RESPONSE_MSG_UNEXPECTED_ERROR = 'Unxpected error'
RESPONSE_MSG_USER_ALREADY_EXISTS = 'User already exists'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tp_databases.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tp_databases.wsgi.application'


DATABASES = {
    # Temp db for develop
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
