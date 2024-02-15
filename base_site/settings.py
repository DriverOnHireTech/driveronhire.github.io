import os
from pathlib import Path
import environ
from firebase_admin import initialize_app
import firebase_admin
from firebase_admin import credentials, initialize_app

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# GEOS_LIBRARY_PATH = 'D:\driveronhire.github.io\env\Lib\site-packages\geos'
# GDAL_LIBRARY_PATH = 'D:\driveronhire.github.io\env\Lib\site-packages\GDAL-3.4.3.dist-info'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-q&qhlk_^z#n5nqmymkrezl(2c7unn3qw_g7ok(+!w#6gnzq7ab"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['18.224.98.224','*']
AUTH_USER_MODEL='authentication.User'
#AUTHENTICATION_BACKENDS = ('base_site.backend.AuthBackend',) # Custome auth model



CORS_ORIGIN_ALLOW_ALL=False

CSRF_TRUSTED_ORIGINS=[
    'https://driversonhire.com',
    'https://d2nevejjxy6v7u.cloudfront.net' #.com
    'https://driveronhire.com'
    'https://www.driveronhire.com'
    'https://d3m71pi62oje9c.cloudfront.net' #driversonhire.in
    'http://ec2-18-224-98-224.us-east-2.compute.amazonaws.com'

]

# SECURE_SSL_REDIRECT=True

# Application definition

INSTALLED_APPS = [
    "channels",
    "jazzmin",
    "authentication",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "rest_framework",
    'corsheaders',
    "drf_spectacular",
    "booking",
    "user_master",
    "driver_management",
    "client_management",
    "enquiry",
    "django_filters",
    #'multiselectfield',
    
    "fcm_django",
    "rest_framework.authtoken",
    "storages",
    "rest_framework_gis"
   
   
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddl`eware',
    'django.middleware.common.CommonMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000', # Local frontend
    'https://driversonhire.com', # Backend
    'http://ec2-18-224-98-224.us-east-2.compute.amazonaws.com', # Backend
    'https://d2nevejjxy6v7u.cloudfront.net',  # Website frontend
    'http://driveronhire.s3-website.ap-south-1.amazonaws.com', # CRM LINK
    'https://d3m71pi62oje9c.cloudfront.net', #driversonhire.in
    'https://driversonhire.in',
    'https://driveronhire.com',
    'https://www.driveronhire.com',
    'http://driveronhire.com.s3-website.us-east-2.amazonaws.com' #driveronhire.com 

)

ROOT_URLCONF = "base_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#WSGI_APPLICATION = "base_site.wsgi.application"
ASGI_APPLICATION = "base_site.asgi.application"


env = environ.Env()
# reading .env file
environ.Env.read_env()
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT':env('DATABASE_PORT'),
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT=BASE_DIR/ "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#STATICFILES_DIRS=[os.path.join(BASE_DIR, 'dohfrontend/build/static')]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication' ],
    
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 25,  
}

#Setup for push notification with firebase

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, "notification.json")
# cred = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
cred = credentials.Certificate(os.path.join(BASE_DIR, "notification.json"))
initialize_app(cred, options={
    "projectId": "notification-1c61d",
    "messagingSenderId": "601537089473",
})

FCM_DJANGO_SETTINGS = {

    "DEFAULT_FIREBASE_APP": None,
    "APP_VERBOSE_NAME": "django_fcm",
    "FCM_SERVER_KEY": "AAAAjA5nj8E:APA91bGPmqvxPcz6S148QFNeiq04m6GrNsO1jb72d-HLD0NDD9hB3kJ4ytIuRDwIZEWIYKKKwnEUb3TTOgC-ocMY92XLEgKhnt4qLQJCt2LW3lv9Vb5TUlilzU1EZfF0mizEHOwN-tfv",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}

# PUSH_NOTIFICATIONS_SETTINGS = {
#         "FCM_API_KEY": "[your api key]",
#         "GCM_API_KEY": "[your api key]",
#         "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
# }


CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "X-CSRFToken"

# GDAL_LIBRARY_PATH = '/opt/homebrew/opt/gdal/lib/libgdal.dylib'
# GEOS_LIBRARY_PATH = '/opt/homebrew/opt/geos/lib/libgeos_c.dylib'

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True


# AWS Bucket for images storage
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME=env('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
AWS_S3_VERUFY=True
DFAULT_FILE_STORAGE='storage.backends.s3boto3.S3BotoStorage'

# Twilio account settings
TWILIO_ACCOUNT_SID = 'AC5c39741c6c06ec1915938a3065465e46'
TWILIO_AUTH_TOKEN = 'a1715dfe516b118117334960626c30ca'
TWILIO_PHONE_NUMBER = '+12107141446'


#Email Send setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'enquiry.driveronhire@gmail.com'
EMAIL_HOST_PASSWORD = 'vnunfrjriwdctbhj'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# calling gupshup user&pass
user_id=env('user_id')
password=env('password')

# CRONJOBS = [
#     ('*/1 * * * *', 'booking.cron.print_hello')
# ]
