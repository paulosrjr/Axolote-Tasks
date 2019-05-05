from __future__ import absolute_import, unicode_literals
import subprocess
from actions import celery_app, logger, test_none


class Rsync(celery_app.Task):
    """
    Execute a Rsync Backup
    """
    def __init__(self):
        self.name = "actions.backup_executors.common.rsync"
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
        pass


celery_app.register_task(Rsync())
