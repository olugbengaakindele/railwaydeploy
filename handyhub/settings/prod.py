from .base import *
import os
from pathlib import Path
import dj_database_url

DEBUG = False


LOGGING = {}
LOGGING_CONFIG = None

os.environ.get("SECRET_KEY", "")

ALLOWED_HOSTS =  ["*"]
# raw_hosts = os.environ.get("ALLOWED_HOSTS", "")
# print("RAW ALLOWED_HOSTS =", repr(raw_hosts))

# ALLOWED_HOSTS = [
#     h.strip()
#     for h in raw_hosts.split(",")
#     if h.strip()
# ]

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if os.environ.get("CSRF_TRUSTED_ORIGINS") else []

# ✅ Production database (start simple with SQLite for staging if you want)
# # Option A (staging quick): SQLite
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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

    "django.contrib.sessions.middleware.SessionMiddleware",   # ✅ must be before auth
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",  # ✅ required
    "django.contrib.messages.middleware.MessageMiddleware",     # ✅ required

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # ✅ your custom middleware should be AFTER auth (so request.user exists)
    "users.middleware.UpdateLastSeenMiddleware",
]
