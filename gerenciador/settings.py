import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (if present)
load_dotenv(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Default for development only if not provided
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-insecure-key-change-me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('1', 'true', 'yes')

# Suporte a nomes alternativos de variáveis de ambiente
_allowed_hosts_raw = os.getenv('DJANGO_ALLOWED_HOSTS') or os.getenv('ALLOWED_HOSTS') or 'localhost,127.0.0.1'
# Fallback para Azure App Service: WEBSITE_HOSTNAME é definido automaticamente
_website_hostname = os.getenv('WEBSITE_HOSTNAME', '').strip()
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(',') if h.strip()]
if _website_hostname and _website_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_website_hostname)
# Fallback específico para o subdomínio custom do projeto (evita 400 quando não há App Settings)
_custom_subdomain = 'tutorialdjangovscode.stela.tec.br'
if _custom_subdomain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_custom_subdomain)

# CSRF settings
# Ensure that the CSRF trusted origins are set correctly for your production domain
# This is important for security, especially when using CSRF protection in forms
# Replace with your actual domain if different

# CSRF_TRUSTED_ORIGINS is used to specify which origins are trusted for CSRF protection
# This is particularly important when your application is served over HTTPS
# and you want to ensure that CSRF tokens are validated against trusted origins.
# The following line should be updated with your actual domain if different.

_csrf_origins_raw = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '') or os.getenv('CSRF_TRUSTED_ORIGINS', '')
if _csrf_origins_raw:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins_raw.split(',') if o.strip()]
else:
    # Se não informado, usar o host do Azure (se disponível) com https como trusted origin
    CSRF_TRUSTED_ORIGINS = [f"https://{_website_hostname}"] if _website_hostname else []
    # Garantir também o subdomínio custom em produção
    if _custom_subdomain:
        CSRF_TRUSTED_ORIGINS.append(f"https://{_custom_subdomain}")

# Proxy/HTTPS (Azure): reconhecer HTTPS real quando atrás do proxy do App Service
_proxy_header_raw = os.getenv('SECURE_PROXY_SSL_HEADER', '').strip()
if _proxy_header_raw:
    _ph = [p.strip() for p in _proxy_header_raw.split(',', 1)]
    if len(_ph) == 2 and _ph[0] and _ph[1]:
        SECURE_PROXY_SSL_HEADER = (_ph[0], _ph[1])
elif _website_hostname:
    # Valor padrão em Azure App Service
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Permitir habilitar via env sem default agressivo
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() in ('1', 'true', 'yes')
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() in ('1', 'true', 'yes')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notas',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Middleware for serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gerenciador.urls'

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

WSGI_APPLICATION = 'gerenciador.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# Database configuration using environment variables
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
if DB_ENGINE == 'django.db.backends.mysql':
    # Se DB_SSL_CA estiver vazio ou não definido, usar o certificado padrão incluso no projeto
    _db_ssl_ca_env = os.getenv('DB_SSL_CA')
    _db_ssl_ca_value = str(BASE_DIR / 'gerenciador' / 'DigiCertGlobalRootG2.crt.pem') if not _db_ssl_ca_env or not _db_ssl_ca_env.strip() else _db_ssl_ca_env
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', ''),
            'USER': os.getenv('DB_USER', ''),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', ''),
            'PORT': os.getenv('DB_PORT', '3306'),
            # Reutiliza conexões com o banco (opcional). 0 = desativado
            'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', '0')),
            'OPTIONS': {
                'ssl': {
                    'ssl-ca': _db_ssl_ca_value
                }
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'CONN_MAX_AGE': int(os.getenv('DB_CONN_MAX_AGE', '0')),
        }
    }
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Whitenoise configuration for serving static files in production
# https://whitenoise.evans.io/en/stable/django.html
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
