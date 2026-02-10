from .base import *
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv


DEBUG = False


LOGGING = {}
LOGGING_CONFIG = None

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing on Railway")

ALLOWED_HOSTS =  ["*"]

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if os.environ.get("CSRF_TRUSTED_ORIGINS") else []

if DB_LIVE not in ["False", False]:
    
    DATABASE = {
        'default' : {
            'ENGINE': 'django.db.backends.pstgresql',
            'NAME' : os.getenv("DB_NAME"),
            'USER' : os.getenv("DB_USER"),
            'PASSWORD' : os.getenv("DB_PASSWORD"),
            'HOST' : os.getenv("DB_HOST"),
            'PORT':  os.getenv("DB_PORT"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE' :'django.db.backends.sqlite3' ,
            'NAME' : BASE_DIR / 'db.sqlite3' ,
        }
    }

# Security (enable when you're behind HTTPS)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Email (env-based)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "LocalTradePros <noreply@localtradespro.ca>")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware" ,

    "django.contrib.sessions.middleware.SessionMiddleware",   # ✅ must be before auth
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",  # ✅ required
    "django.contrib.messages.middleware.MessageMiddleware",     # ✅ required

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # ✅ your custom middleware should be AFTER auth (so request.user exists)
    "users.middleware.UpdateLastSeenMiddleware",
]
