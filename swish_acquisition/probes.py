"""
Probes which detect service health
"""
import logging

from sqlalchemy.sql import text

from swish_acquisition.celery_app import app
from swish_acquisition.session import managed_session
from swish_acquisition.s3 import S3_CLIENT


__all__ = ['detect_dependent_services']


logger = logging.getLogger(__name__)


def logging_probe(func):

    def _wrapper(*args, **kwargs):
        logger.info(f'{func.__name__}, start')
        try:
            func(*args, **kwargs)
            logger.info(f'{func.__name__}, done')
        except:  # NOQA
            logger.info(f'{func.__name__}, meets error')
            raise

    return _wrapper


@logging_probe
def _detect_postgres():
    with managed_session() as session:
        session.execute(text('SELECT 1'))


@logging_probe
def _detect_rabbitmq():
    with app.connection_for_read() as conn:
        channel = conn.channel()
        # Channel objects
        # from pyamqp.Channel (e.g. RabbitMQ) and virtual.Channel (e.g. Redis)
        # have different properties
        if hasattr(channel, 'is_open'):
            is_channel_open = channel.is_open
        else:
            is_channel_open = not channel.closed
        if not is_channel_open:
            raise


@logging_probe
def _detect_minio():
    S3_CLIENT.bucket_exists('detect-used-virtual-bucket')


def detect_dependent_services():
    """
    Please register 'detect' methods here
    """
    _detect_postgres()
    _detect_rabbitmq()
    _detect_minio()
