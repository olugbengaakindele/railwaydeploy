from .base import *
import os
from pathlib import Path
import dj_database_url


DEBUG = True

# For local dev, a fallback key is okay (but best to set env var)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-unsafe-secret-key")

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")

# Usually not needed locally unless you're testing https/domains
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if os.environ.get("CSRF_TRUSTED_ORIGINS") else []

# ✅ Your current local DB (SQL Server) - keep for now


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "mssql",
#         "NAME": os.environ.get("DB_NAME", "handyhub"),
#         "HOST": os.environ.get("DB_HOST", r"DESKTOP-CR1OVOB\SQLEXPRESS"),
#         "PORT": os.environ.get("DB_PORT", ""),
#         "OPTIONS": {
#             "driver": os.environ.get("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
#             "encrypt": os.environ.get("DB_ENCRYPT", "no"),
#             "trust_server_certificate": os.environ.get("DB_TRUST_CERT", "yes"),
#         },
#     }
# }

# Email - safer local option (prints emails to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "LocalTradePros <noreply@local>")

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
