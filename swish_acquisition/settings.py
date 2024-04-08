"""
settings
"""


DEBUG = False


DATABASES = {
    'swish_analytics': {
        'ENGINE': 'postgresql+psycopg2',
        'NAME': 'swish_analytics',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432
    }
}


# retry upper limit when init backend tables
PREPARE_MODELS_MAX_RETRIES = 3
