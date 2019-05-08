import sys
import os
from pytest import raises
import unittest
from celery.exceptions import Retry

modules_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, modules_path + '/../')

from actions.backup_executors.common.simple_test import SimpleTest


class TestScp(unittest.TestCase):
    def setUp(self):
        simple_test = SimpleTest()
        self.task = simple_test.apply_async()
        self.results = self.task.get()

    def test_task_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')
