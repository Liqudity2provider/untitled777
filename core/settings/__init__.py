import os

ENVIRONMENT = 'locale'


if ENVIRONMENT == 'locale':
    from .local import *
elif ENVIRONMENT == 'production':
    from .production import *
else:
    from .settings import *

