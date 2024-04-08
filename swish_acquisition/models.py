"""
Database models used by SQLAlchemy, which store results
"""
from enum import Enum
import json
import logging
import time

from sqlalchemy import Date, DateTime, event, String, text
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import DDL

from swish_acquisition.conf import settings
from swish_acquisition.session import managed_session


logger = logging.getLogger(__name__)


class Status(Enum):

    CREATED = 'CREATED'  # received trigger request
    PENDING = 'PENDING'  # submitted to Celery
    IN_PROGRESS = 'IN_PROGRESS'  # have begun to execute
    SUCCESS = 'SUCCESS'  # success
    FAILURE = 'FAILURE'  # failure

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        raise NotImplementedError


IMPLICIT_COLUMN_NAMES = [
    'created_time',
    'updated_time'
]
CREATE_FUNCTION_UPDATED_TIME_TRIGGER = DDL("""
    CREATE OR REPLACE FUNCTION trigger_set_updated_time() RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_time = NOW();
            RETURN NEW;
        END;
    $$ LANGUAGE plpgsql;
""")
UPDATE_TIME_TRIGGER_DDL_FORMAT = """
    CREATE OR REPLACE TRIGGER on_update_{table_name}
        BEFORE UPDATE
        ON {table_name}
        FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_updated_time();
"""


class BaseModel(DeclarativeBase):

    __abstract__ = True

    created_time: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=False,
        server_default=text('TIMEZONE(\'utc\', CURRENT_TIMESTAMP)'),
        doc='Time when the record was created',
        comment='Time when the record was created')
    updated_time: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=False,
        server_default=text('TIMEZONE(\'utc\', CURRENT_TIMESTAMP)'),
        doc='Time when the record was updated',
        comment='Time when the record was updated')


class SwishPipeline(BaseModel):

    __tablename__ = 'swish_pipeline'

    pipeline_id: Mapped[str] = mapped_column(
        String(128), primary_key=True,
        server_default=text('uuid_generate_v4()'),
        doc='Identifier of the pipeline',
        comment='Identifier of the pipeline'
    )
    game_date: Mapped[Date] = mapped_column(
        Date, nullable=False,
        doc='Date of game',
        comment='Date of game'
    )
    league_id: Mapped[str] = mapped_column(
        String(128), nullable=False,
        server_default='00',
        doc='Identifier of league',
        comment='Identifier of league'
    )
    pipeline_status: Mapped[str] = mapped_column(
        String(128), nullable=False,
        server_default=Status.CREATED.value,
        doc='Status of the pipeline with enum value',
        comment='Status of the pipeline with enum value'
    )
    started_time: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=True,
        doc='Time when the pipeline started',
        comment='Time when the pipeline started'
    )
    completed_time: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=True,
        doc='Time when the pipeline completed',
        comment='Time when the pipeline completed'
    )


class SwishTask(BaseModel):

    __tablename__ = 'swish_task'

    pipeline_id: Mapped[str] = mapped_column(
        String(128), primary_key=True,
        doc='Identifier of the pipeline',
        comment='Identifier of the pipeline')
    task_id: Mapped[str] = mapped_column(
        String(128), primary_key=True,
        server_default=text('uuid_generate_v4()'),
        doc='Identifier of the task',
        comment='Identifier of the task')
    task_name: Mapped[str] = mapped_column(String(320), nullable=True)
    celery_task_id: Mapped[str] = mapped_column(
        String(128), nullable=True,
        doc='Identifier of the Celery task',
        comment='Identifier of the Celery task')
    parent_task_id: Mapped[str] = mapped_column(
        String(128), nullable=True,
        doc='Identifier of the task\'s parent',
        comment='Identifier of the task\'s parent')
    task_arguments: Mapped[str] = mapped_column(
        String, nullable=False,
        server_default='{}', default=json.dumps({}),
        doc='Arguments of the task as JSON string',
        comment='Arguments of the task as JSON string')
    task_status: Mapped[str] = mapped_column(
        String(128), nullable=False,
        server_default=Status.CREATED.value,
        doc='Status of the task with enum value',
        comment='Status of the task with enum value')
    started_time: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=True,
        doc='Time when the task started',
        comment='Time when the task started')
    completed_time: Mapped[DateTime] = mapped_column(
        DateTime(True), nullable=True,
        doc='Time when the task completed',
        comment='Time when the task completed')


event.listen(BaseModel.metadata, 'before_create', CREATE_FUNCTION_UPDATED_TIME_TRIGGER)


def prepare_models():
    retries = 0
    while True:
        try:
            with managed_session() as session:
                BaseModel.metadata.create_all(session.bind)
        except DatabaseError:
            if retries < settings.PREPARE_MODELS_MAX_RETRIES:
                logger.warning(f'met some issues when try to initialize tables, '
                               f'would go to {retries + 1} retry')
                time.sleep(10)
                retries += 1
            else:
                raise
        else:
            break
