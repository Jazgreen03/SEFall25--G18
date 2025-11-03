"""
Django settings for SecondServe project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import sys

# -------------------------------------------------------------------
# BASE DIR & Load .env
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
# Load .env from BASE_DIR or its parent
dotenv_path = BASE_DIR / ".env"
if not dotenv_path.exists():
    dotenv_path = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path)

# -------------------------------------------------------------------
# SECURITY
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dummy-secret-key-for-dev")
DEBUG = True
# ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(",")
ALLOWED_HOSTS = ['*']

# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "SecondServe.apps.MongoAdminConfig",
    "SecondServe.apps.MongoAuthConfig",
    "SecondServe.apps.MongoContentTypesConfig",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "User",
    "Inventory",
    "Organization",
    "corsheaders",  # Enable CORS support
]

# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Must be at the top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "SecondServe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "SecondServe.wsgi.application"

# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django_mongodb_backend",
        "HOST": os.getenv("DATABASE_HOST", "db"),
        "PORT": int(os.getenv("DATABASE_PORT", 27017)),
        "NAME": os.getenv("DATABASE_NAME", "SecondServe"),
        "USER": os.getenv("DATABASE_USERNAME", ""),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
        "OPTIONS": {"authSource": os.getenv("DATABASE_AUTH_SOURCE", "admin")},
        "TEST": {"NAME": os.getenv("DATABASE_TEST_NAME", "SecondServe_test")},
    },
}

DATABASE_ROUTERS = ["django_mongodb_backend.routers.MongoRouter"]

# -------------------------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "User.User"

# -------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# STATIC FILES
# -------------------------------------------------------------------
STATIC_URL = "/static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django_mongodb_backend.fields.ObjectIdAutoField"

# MongoDB-specific Migration Modules
MIGRATION_MODULES = {
    "admin": "mongo_migrations.admin",
    "auth": "mongo_migrations.auth",
    "contenttypes": "mongo_migrations.contenttypes",
}

# -------------------------------------------------------------------
# CORS SETTINGS (fix preflight and Angular dev)
# -------------------------------------------------------------------
# Allow localhost:4200 (Angular dev server) or all origins during dev
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:4200",
    ]

CSRF_TRUSTED_ORIGINS = ["http://localhost:4200"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = [
    "content-type",
    "x-csrftoken",  # <-- Add this
    "accept",
    "authorization",
    "x-requested-with",
    "accept-encoding",
    "origin",
    "user-agent",
    "accept-language",
    "dnt",
    "cache-control",
    "pragma",
]

# Optional: disable automatic slash redirect for APIs
APPEND_SLASH = True  # Or False if you want URLs without trailing slash

# -------------------------------------------------------------------
# DEBUG OUTPUT (optional)
# -------------------------------------------------------------------
if DEBUG:
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"Loaded .env from: {dotenv_path}")
    print(f"DATABASES: {DATABASES}")
