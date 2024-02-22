"""
Celery application
"""
from typing import Any

from celery import Celery
from celery.signals import setup_logging

from swish_acquisition.logging_config import config_logging


app = Celery(main=__name__)
app.config_from_object('swish_acquisition.celeryconfig')


@setup_logging.connect
def config_loggers(*args: Any, **kwargs: Any) -> None:  # NOQA
    config_logging('swish-acquisition')


if __name__ == '__main__':
    app.start()
