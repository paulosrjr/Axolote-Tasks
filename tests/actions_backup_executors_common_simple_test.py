import sys
import os
from pytest import raises
import unittest
from celery.exceptions import Retry

modules_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, modules_path + '/../')

from actions.backup_executors.common.scp import Scp


class TestScp(unittest.TestCase):
    def setUp(self):
        ka = {
        "scp_type": "key",
        "key": "/home/{}/.ssh/key".format(os.getenv('USER_TEST', 'travis')),
        "password": "password",
        "parameters": "-r -o IdentitiesOnly=yes",
        "username": "{}".format(os.getenv('USER_TEST', 'travis')),
        "host": "localhost",
        "remotepath": "/home/{}/.ssh".format(os.getenv('USER_TEST', 'travis')),
        "localpath": "/tmp/scp_test"
        }

        scp_task = Scp()
        self.task = scp_task.apply_async(kwargs=ka, queue="axolote", exchange="axolote", routing_key="axolote")
        self.results = self.task.get()

    def test_task_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')
