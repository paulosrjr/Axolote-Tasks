import sys
from pytest import raises
import unittest
from celery.exceptions import Retry
from actions.backup_executors.scp import Scp


class TestScp(unittest.TestCase):
    def setUp(self):
        ka = {
        "scp_type": "key", 
        "key": "/home/test/.ssh/key", 
        "password": "password", 
        "parameters": "-r -o IdentitiesOnly=yes", 
        "username": "test",
        "ip": "127.0.0.1",
        "remotepath": "/home/test",
        "localpath": "/tmp/test"
        }

        scp_task = Scp()
        self.task = scp_task.apply_async(kwargs=ka, queue="axolote", exchange="axolote", routing_key="axolote")
        self.results = self.task.get()

    def test_task_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')