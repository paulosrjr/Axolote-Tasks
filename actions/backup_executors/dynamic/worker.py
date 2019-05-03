from __future__ import absolute_import, unicode_literals
from time import sleep
import sys
import subprocess
from actions import celery_app, logger, test_none

class DynamicWorker(celery_app.Task):
    """
    Execute a task from backup with dynamic specification
    """
    def __init__(self):
        self.name = "actions.backup_executors.dynamic.worker"
        self.message = ""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r} message: {2!r}'.format(task_id, exc, self.message))

    def on_success(self, retval, task_id, args, kwargs):
        print('{0!r} success: {1!r} message: {2!r}'.format(task_id, retval, self.message))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} retry: {1!r}'.format(task_id, exc))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print('{0!r} finished with: {1!r}'.format(task_id, status))

    def run(self, **kwargs):
        client_specification = kwargs.get('client_specification')
        try:
            print(client_specification)
        except Exception:
            raise NotImplementedError()


celery_app.register_task(Scp())
