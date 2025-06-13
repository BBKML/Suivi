from pathlib import Path
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité : secret key en variable d'environnement
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'change-this-secret-key-in-production')

# Mode développement (à désactiver en production)
DEBUG = True

# Hôtes autorisés (mettre le domaine en production)
ALLOWED_HOSTS = []

# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'Suiv.CustomUser'

# Applications Django
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Suiv',  # Ton application principale
    'widget_tweaks',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Fichiers de templates
ROOT_URLCONF = 'Suivi.urls'  # Conservé "Suivi" comme nom du projet

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Assurez-vous que le dossier templates existe
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

# Application WSGI
WSGI_APPLICATION = 'Suivi.wsgi.application'  # Conservé "Suivi" comme nom du projet

# Base de données (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Langue et fuseau horaire
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques
STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]


# Configuration des fichiers médias
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Localisation
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

# Configuration de l'authentification
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = '/admin/'

# Paramètres de sécurité pour le développement (à renforcer en production)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Configuration des e-mails (utilisation de variables d'environnement)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Journalisation (logging)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# Django Jazzmin (interface admin personnalisée)
JAZZMIN_SETTINGS = {
    "show_ui_builder": True,
    "site_title": "Suivi",
    
    "site_brand": "Nangui Abrogoua",
    "welcome_sign": "Bienvenue sur l'interface de gestion des suivis",
    "site_logo": "logo.jpeg",  # Assurez-vous que ce fichier existe dans le dossier static
    "search_model": "Suiv.SuiviEnseignement",
    "copyright": "Mon Site",
    "language_chooser": True,
  
    "custom_links": {
        "Suiv.SuiviEnseignement": [
            {
                "name": "Exporter en CSV",
                "url": "admin:Suiv_suivienseignement_export_csv",
                "icon": "fas fa-file-csv",
                "permissions": ["Suiv.view_suivienseignement"]
            }
        ],
        "Suiv.Cours": [
            {
                "name": "Imprimer un Cours",
                "url": "admin:Suiv_cours_imprimer_cours",
                "icon": "fas fa-print",
                "permissions": ["Suiv.view_cours"]
            }
        ],
         "Suiv.Enseignant": [
            {
                "name": "Imprimer Enseignants Paginé",
                "url": "admin:Suiv_enseignant_imprimer_enseignants_paginated",
                "icon": "fas fa-print",
                "permissions": ["Suiv.view_enseignant"]
            }
        ],
    },
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "Suiv.CustomUser": "fas fa-user-circle",
        "Suiv.Grade": "fas fa-graduation-cap",
        "Suiv.Salle": "fas fa-building",
        "Suiv.Statut": "fas fa-check-circle",
        "Suiv.AnneeAcademique": "fas fa-calendar-alt",
        "Suiv.Enseignant": "fas fa-chalkboard-teacher",
        "Suiv.NiveauEtude": "fas fa-layer-group",
        "Suiv.GroupeEtudiant":"fas fa-users",
        "Suiv.Semestre": "fas fa-calendar",
        "Suiv.Cours": "fas fa-book",
        "Suiv.SuiviEnseignement": "fas fa-clipboard-list",
        "Suiv.Enseigner": "fas fa-chalkboard",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "simplex",
    "custom_css": "static/css/jazzmin_custom.css",
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'