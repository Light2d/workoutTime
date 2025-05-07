

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d*+sh_4vm7a2eikx&8go81#z8j$bbb5db_c91kfy*=o9s0o5c)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['e9532f16259f5a9e64bf521fbc4aa20b.serveo.net', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = [
    'https://e9532f16259f5a9e64bf521fbc4aa20b.serveo.net',
]

# Application definition

INSTALLED_APPS = [ 
    "workoutTimeApp",
    'dashboard',
    'forum',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'social_django',
    'tinymce',
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'workoutTime.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'workoutTimeApp.context_processors.unread_notifications_count',

            ],
        },
    },
]

WSGI_APPLICATION = 'workoutTime.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = 'media/'  
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'workoutTimeApp.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lightpavelll@gmail.com'
EMAIL_HOST_PASSWORD = 'ydzi apdw exgw mmjr'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
SITE_URL = 'http://127.0.0.1:8000'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_VK_OAUTH2_KEY = '53013207'  # ID приложения ВК
SOCIAL_AUTH_VK_OAUTH2_SECRET = '0VvVGOVhClEKqOXszeYa'  # Секретный ключ приложения

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', 'user_info', 'bdate', 'photos',]
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['bdate', 'photo_200', 'email']

SOCIAL_AUTH_VK_OAUTH2_REDIRECT_URI =  'https://6551690d90f5b9.lhr.life/complete/vk-oauth2/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'workoutTimeApp.vk.save_user_info',
    'social_core.pipeline.user.user_details',
    'workoutTimeApp.vk.activate_user',
)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'


