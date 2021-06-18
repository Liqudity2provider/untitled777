import environ

env = environ.Env()
environ.Env.read_env()

ENVIRONMENT = env("ENVIRONMENT")

if ENVIRONMENT == 'locale':
    from .local import *
elif ENVIRONMENT == 'production':
    from .production import *
else:
    from .settings import *

