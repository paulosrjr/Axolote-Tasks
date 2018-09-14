import os

broker_url = "redis://{}:{}/{}".format(os.getenv('REDIS_HOST', 'localhost'), os.getenv('REDIS_PORT', '6379'), os.getenv('REDIS_DB', '0'))
result_backend = "redis://{}:{}/{}".format(os.getenv('REDIS_HOST', 'localhost'), os.getenv('REDIS_PORT', '6379'), os.getenv('REDIS_DB', '0'))

#task_serializer = 'json'
#task_default_exchange_type = 'direct'
#task_default_delivery_mode = 'persistent'
#task_ignore_result = False

task_queues = {
    'axolote': {
        'exchange': 'axolote',
        'routing_key': 'axolote',
    }
}

include = [
    'actions.backup_executors.scp',
]