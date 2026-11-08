"""Local development settings."""

from config.settings.base import *  # noqa: F403

DEBUG = env.bool("DEBUG", default=True)  # noqa: F405

# Trust TLS terminated by a local reverse proxy or demo tunnel (ngrok).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# ngrok hostnames change on each free session; leading-dot matches subdomains.
_tunnel_hosts = [
    ".ngrok-free.app",
    ".ngrok.app",
    ".ngrok.io",
    ".ngrok-free.dev",
    ".ngrok.dev",
    ".lhr.life",
    ".localhost.run",
]
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS + _tunnel_hosts))  # noqa: F405

# Allow common local host/port combinations for admin login CSRF checks.
_dev_csrf_origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.ngrok-free.app",
    "https://*.ngrok.app",
    "https://*.ngrok.io",
    "https://*.ngrok-free.dev",
    "https://*.ngrok.dev",
    "https://*.lhr.life",
    "https://*.localhost.run",
]
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS + _dev_csrf_origins))  # noqa: F405

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += [  # noqa: F405
    "rest_framework.renderers.BrowsableAPIRenderer"
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
