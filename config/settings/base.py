import environ

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (django_security_headers_example/config/settings/base.py - 3 =
# django_security_headers_example/)
APPS_DIR = ROOT_DIR.path("django_security_headers_example")

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in
    # the .env file, that is to say variables from the .env files will only be used if
    # not defined as environment variables.
    env_file = str(ROOT_DIR.path(".env"))
    print("Loading : {}".format(env_file))
    env.read_env(env_file)
    print("The .env file has been loaded. See base.py for more information\n")

# APP CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Default Django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    # Useful template tags:
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    # Admin
    "django.contrib.admin",
    "django_security_headers_example.core"
]

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_security_headers_example.core.middleware.SecurityHeaderMiddleware",
    "django_feature_policy.FeaturePolicyMiddleware",
    "csp.contrib.rate_limiting.RateLimitedCSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Steven Pate""", "steven@laac.dev")]

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Enables {{ CSP_NONCE }} in templates
                "csp.context_processors.nonce",
            ],
        },
    }
]

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#run-manage-py-check-deploy

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True

# https://django-csp.readthedocs.io/en/latest/configuration.html
CSP_DEFAULT_SRC = ["'none'"]
# Try to remove unsafe-inline in the future
CSP_STYLE_SRC = [
    "'self'",
    "https://fonts.googleapis.com",
]
CSP_UPGRADE_INSECURE_REQUESTS = not DEBUG
CSP_REPORT_URI = env.list("CSP_REPORT_URI")
CSP_REPORT_PERCENTAGE = env.float("CSP_REPORT_PERCENTAGE", default=0.6)
CSP_FORM_ACTION = ["'self'"]
CSP_BASE_URI = ["'none'"]
CSP_FRAME_ANCESTORS = ["'none'"]
CSP_OBJECT_SRC = ["'none'"]
CSP_FRAME_SRC = [
    "'self'",
    "https://www.gstatic.com/recaptcha/",
]
CSP_SCRIPT_SRC = [
    "'self'",
    "https://www.google.com/recaptcha/",
    "https://www.gstatic.com/recaptcha/",
]
CSP_MANIFEST_SRC = ["'self'"]
CSP_CONNECT_SRC = [
    "'self'",
]
CSP_IMG_SRC = [
    "'self'",
]
CSP_FONT_SRC = ["'self'", "https://fonts.googleapis.com", "https://fonts.gstatic.com"]
CSP_INCLUDE_NONCE_IN = ["script-src"]

REFERRER_POLICY = "strict-origin-when-cross-origin"
EXPECT_CT_MAX_AGE = env.int("EXPECT_CT_MAX_AGE")
EXPECT_CT_ENFORCE = env.bool("EXPECT_CT_ENFORCE")
EXPECT_CT_REPORT_URI = env("EXPECT_CT_REPORT_URI")

# https://github.com/adamchainz/django-feature-policy
FEATURE_POLICY = {"microphone": "none", "speaker": "none"}
