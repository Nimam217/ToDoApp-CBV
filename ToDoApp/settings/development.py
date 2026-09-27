from .base import *


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp4dev"  # SMTP server host
EMAIL_PORT = 25  # SMTP server port (587 for TLS, 465 for SSL)
EMAIL_HOST_USER = ""  # SMTP server username
EMAIL_HOST_PASSWORD = ""  # SMTP server password
EMAIL_USE_TLS = False