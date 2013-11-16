import os

from foodroulette_backend.base_settings import *

env = os.getenv('ENVIRONMENT')

if env == 'production':
    from foodroulette_backend.production_settings import *
else:
    from foodroulette_backend.local_settings import *