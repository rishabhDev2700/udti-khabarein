from .base import *

DEBUG = False
ALLOWED_HOSTS = ["udti-khabarein.azurewebsites.net"]
try:
    from .local import *
except ImportError:
    pass
