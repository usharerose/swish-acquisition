"""
Celery configurations
"""
broker_url = 'amqp://rabbitmq:rabbitmq@rabbitmq:5672/rabbitmq'


imports = (
    'swish_acquisition.tasks'
)
