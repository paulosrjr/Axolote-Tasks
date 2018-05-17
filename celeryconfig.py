#broker_url = 'amqp://guest:guest@rabbit:5672//'
broker_url = 'redis://localhost:6379/0'
#result_backend = 'rpc://guest:guest@rabbitmq:5672//'
result_backend = 'redis://localhost:6379/0'
#result_backend = 'mongodb://mongo:27017/celery'

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