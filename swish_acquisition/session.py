"""
Database session manager
"""
from contextlib import contextmanager
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from swish_acquisition.conf import settings


__all__ = ['managed_session']


POOL_SIZE = 5
POOL_RECYCLE = 3600  # 1 hour
POOL_TIMEOUT = 30
STATEMENT_TIMEOUT = 5000


def get_db_uri(db_conf: dict) -> str:
    """
    Get the connection string for the database alias.

    the schema of db_conf is like:
    {
        "ENGINE": "postgresql",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "PORT": 5432,
        "NAME": "postgres"
    }
    """
    return '{dialect}://{username}:{password}@{host}:{port}/{database}'.format(
        dialect=db_conf.get('ENGINE', 'postgresql'),
        username=db_conf['USER'],
        password=quote_plus(db_conf['PASSWORD']),
        host=db_conf['HOST'],
        port=db_conf['PORT'],
        database=db_conf['NAME']
    )


def get_engine(dburi: str, application_name: str = 'swish-acquisition') -> Engine:  # NOQA
    engine_kwargs: dict = {
        'echo': settings.DEBUG,
        'poolclass': QueuePool,
        'pool_size': POOL_SIZE,
        'pool_recycle': POOL_RECYCLE,
        'pool_timeout': POOL_TIMEOUT,
        'connect_args': {
            'options': f'-c statement_timeout={STATEMENT_TIMEOUT}',
            'application_name': application_name
        }
    }
    return create_engine(dburi, **engine_kwargs)


def get_session():
    engine = get_engine(get_db_uri(settings.DATABASES['swish_analytics']))
    session = scoped_session(
        sessionmaker(bind=engine, autoflush=True, expire_on_commit=True)
    )
    return session


SESSION = get_session()


@contextmanager
def managed_session():
    """
    Usage:
        with managed_session() as session:
            session.execute...
    """
    try:
        yield SESSION
        SESSION.commit()
    except:  # NOQA
        SESSION.rollback()
        raise
    finally:
        SESSION.close()
