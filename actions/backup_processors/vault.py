from __future__ import absolute_import, unicode_literals
from time import sleep
import sys
import subprocess
from actions import celery_app, logger, test_none

class VaultAccess(celery_app.Task):
    """
    Execute a Vault access
    """
    def __init__(self):
        self.name = "actions.backup_processors.client"
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
        print(client_specification)



celery_app.register_task(VaultAccess())
