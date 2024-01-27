"""
Celery application
"""
from celery import Celery


app = Celery(main=__name__)
app.config_from_object('swish_acquisition.celeryconfig')
