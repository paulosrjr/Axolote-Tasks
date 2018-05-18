import sys
import os
from pytest import raises
import unittest
from celery.exceptions import Retry
from actions.backup_executors.scp import Scp


class TestScp(unittest.TestCase):
    def setUp(self):
        ka = {
        "scp_type": "key", 
        "key": "/home/travis/.ssh/key", 
        "password": "password", 
        "parameters": "-r -o IdentitiesOnly=yes", 
        "username": "travis",
        "ip": "localhost",
        "remotepath": "/home/travis",
        "localpath": "/tmp/travis"
        }

        scp_task = Scp()
        self.task = scp_task.apply_async(kwargs=ka, queue="axolote", exchange="axolote", routing_key="axolote")
        self.results = self.task.get()

    def test_task_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')