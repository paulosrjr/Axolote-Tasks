import pika
import json
import os
import socket
import uuid

DEFAULT_RABBITMQ_HOST = "localhost"

class RabbitEnqueue(object):
    def __init__(self):
        self.task_id = str(uuid.uuid4())
        self.args = ()
        self.kwargs = {}
        self.__default_task = "worker.actions.build_workflow.BuildWorkflow"
    
    @property
    def default_task(self):
        return self.__default_task

    @default_task.setter
    def default_task(self, task):
        self.__default_task = task

    @property
    def message(self):
        message = json.dumps((self.args, self.kwargs, None))
        return message

    @property
    def headers(self):
        application_headers = {
            'id': self.task_id,
            'lang': 'py',
            'task': self.default_task,
            'argsrepr': repr(self.args),
            'kwargsrepr': repr(self.kwargs),
            'origin': '@'.join([str(os.getpid()), str(socket.gethostname())])
        }
        return application_headers

    @headers.setter
    def headers(self):
        pass

    @property
    def properties(self):
        properties = {
            'correlation_id': self.task_id,
            'content_type': 'application/json',
            'content_encoding': 'utf-8',
        }
        return properties

    def run(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self._rabbit_channel().queue_declare(queue='ict_worker', durable=True, auto_delete=False)

        self._rabbit_channel().basic_publish(exchange='ict_worker',
                                             routing_key='ict_worker',
                                             body=self.message,
                                             properties=pika.BasicProperties(
                                                 delivery_mode=2,
                                                 content_type='application/json',
                                                 content_encoding='utf-8',
                                                 headers=self.headers
                                             ))

    @staticmethod
    def _rabbit_connection():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=DEFAULT_RABBITMQ_HOST))
        return connection

    def _rabbit_channel(self):
        channel = self._rabbit_connection()
        ict_channel = channel.channel()
        return ict_channel