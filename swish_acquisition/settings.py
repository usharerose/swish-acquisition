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
