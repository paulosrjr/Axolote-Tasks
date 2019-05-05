import os
from celery.beat import crontab
from kombu.common import Broadcast
from kombu import Exchange, Queue, binding


if os.getenv('AXOLOTE_BROKER') == "RABBITMQ":
    broker_url = "amqp://{}:{}@{}:{}/{}/".format(os.getenv('RABBIT_USER', 'guest'),
                                                           os.getenv('RABBIT_PASSWORD', 'guest'),
                                                           os.getenv('RABBIT_HOST', 'localhost'),
                                                           os.getenv('RABBIT_PORT', '5672'),
                                                           os.getenv('RABBIT_DB', ''))
else:
    broker_url = "redis://{}:{}/{}".format(os.getenv('REDIS_HOST', 'localhost'),
                                           os.getenv('REDIS_PORT', '6379'),
                                           os.getenv('REDIS_DB', '0'))

if os.getenv('AXOLOTE_BACKEND') == "RABBITMQ":
    result_backend = "rpc://{}:{}@{}:{}/{}/".format(os.getenv('RABBIT_USER', 'guest'),
                                                    os.getenv('RABBIT_PASSWORD', 'guest'),
                                                    os.getenv('RABBIT_HOST', 'localhost'),
                                                    os.getenv('RABBIT_PORT', '5672'),
                                                    os.getenv('RABBIT_DB', ''))
elif os.getenv('AXOLOTE_BACKEND') == "MONGODB":
    if os.getenv('MONGODB_PASSWORD'):
        result_backend = "mongodb://{}:{}@{}:{}/{}".format(os.getenv('MONGODB_USER', 'user'),
                                                           os.getenv('MONGODB_PASSWORD', 'password'),
                                                           os.getenv('MONGODB_HOST', 'localhost'),
                                                           os.getenv('MONGODB_PORT', '27017'),
                                                           os.getenv('MONGODB_DB', 'axolote'))
    else:
        result_backend = "mongodb://{}:{}/{}".format(os.getenv('MONGODB_HOST', 'localhost'),
                                                     os.getenv('MONGODB_PORT', '27017'),
                                                     os.getenv('MONGODB_DB', 'axolote'))
else:
    result_backend = "redis://{}:{}/{}".format(os.getenv('REDIS_HOST', 'localhost'),
                                               os.getenv('REDIS_PORT', '6379'),
                                               os.getenv('REDIS_DB', '0'))


task_serializer = "json"
task_ignore_result = False
task_track_started = True
task_compression = "gzip"
#task_create_missing_queues = True
#task_default_queue = "axolote"
#task_default_delivery_mode = 'persistent'
#task_default_exchange_type = 'direct'
worker_log_color = False
worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s"
worker_lost_wait = 60.0
worker_send_task_events = True
worker_state_db = "axolote_statedb"
worker_redirect_stdouts = True
worker_redirect_stdouts_level = "DEBUG"


include = [
    'actions.backup_executors.common.simple_test',
    'actions.backup_executors.common.scp',
    'actions.backup_executors.common.rsync',
    'actions.backup_executors.ansible.playbook',
]


bcast_exchange = Exchange('bcast', type='direct')
axolote_exchange = Exchange('axolote', type='direct')


task_queues = (
    Broadcast(name='bcast', exchange=bcast_exchange, routing_key='bcast'),
    Queue(name='axolote', exchange=axolote_exchange, routing_key='axolote'),
)


task_routes = {
    'actions.backup_executors.common.simple_test':
        {
            'queue': 'bcast',
            'routing_key': 'bcast',
            'exchange': 'bcast'
         }
}



celery_beat_schedule = {
    'scheduler-task': {
        'task': 'actions.backup_scheduler.scheduler',
        'schedule': crontab(minute='*/1')
    }
}
