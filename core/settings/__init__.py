import os

ENVIRONMENT = os.environ.get("ENVIRONMENT")

if ENVIRONMENT == 'local':
    from .local import *
elif ENVIRONMENT == 'production':
    from .production import *
else:
    from .settings import *

