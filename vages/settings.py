import os
from dotenv import load_dotenv
from decouple import config
from pathlib import Path



# # Load environment variables from .env file
# load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wu&zz4f)fafv(#lauzgc=2(6*+g*lf_86ofltjk2()nm=b&$1r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['Grocery.onrender.com']


# Application definition
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-allauth

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap4',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # Uncomment these if needed
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',

    # Custom apps
    'store',
    'cart',
    'user_authentication',
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  # adds django-allauth
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line for allauth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]
 

ROOT_URLCONF = 'vages.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_processor',
            ],
        },
    },
]


WSGI_APPLICATION = 'vages.wsgi.application'



SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '1052502891637-kt15h6m02gv9rq2ta610urjfa8ohe1r4.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
    
}


SITE_ID = 1  # Define your SITE_ID, typically 1 if you're using a single site
LOGIN_REDIRECT_URL = '/'  # redirect after login
LOGOUT_REDIRECT_URL = '/'  # redirect after logout

# Configure additional django-allauth settings (optional)
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#Static
STATIC_URL = '/static/'

if not DEBUG:
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static'),]

WHITENOISE_USE_FINDERS =True
#Media
MEDIA_URL ='/media/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type

# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# settings.py


# settings.py

MPESA_SHORTCODE = 'your_shortcode_here'  # Ensure this is set
MPESA_CONSUMER_KEY = '2Qr4mtdteydnub1082EfNAmeSEAKKP9FFknTMBGhTGfwGkGg'  # Ensure this is set
MPESA_CONSUMER_SECRET = 'yCQM2ReEKvDyV1L7HLjACVqtHj3GLw8MUtaRaZ6rURoz6pBbLbRqLOz4NAIN3uz8iuu9i8ounloiuhdrlofjenfdjshn'  # Ensure this is set
CALLBACK_URL = 'https://yourdomain.com/path/to/callback/'  # Ensure this is set


# print(f'M-PESA Consumer Key: {MPESA_CONSUMER_KEY}')
# print(f'M-PESA Consumer Secret: {MPESA_CONSUMER_SECRET}')
# print(f'M-PESA Shortcode: {MPESA_SHORTCODE}')
# print(f'Callback URL: {CALLBACK_URL}')

from decouple import config
import paypalrestsdk

PAYPAL_CLIENT_ID = 'Af2F9Obv-yG7_frIkxQIIlBQ8rdHasyb__YMg6QvRP5iAPnZ6wVAfiVLoNhR_hokbwsYUrzotLf4gRPl'
PAYPAL_SECRET = 'EBGRQHRHWYdL-EnSLCiWYB5us2MxQlAkFuQCV3IThzAwD9l0ivE-dY1Z3yoEDd6GnO5jJYQCqzcTY3_5'

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" in production
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_SECRET,
})
    
