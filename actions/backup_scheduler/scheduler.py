from __future__ import absolute_import, unicode_literals
from time import sleep
import sys
import subprocess
from actions import celery_app, logger, test_none


class BackupScheduler(celery_app.Task):
    """
    Run every minute searching backups to execute
    """
    def __init__(self):
        self.name = "actions.backup_scheduler.scheduler"
        self.message = ""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r} message: {2!r}'.format(task_id, exc, self.message))

    def on_success(self, retval, task_id, args, kwargs):
        print('{0!r} success: {1!r} message: {2!r}'.format(task_id, retval, self.message))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} retry: {1!r}'.format(task_id, exc))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print('{0!r} finished with: {1!r}'.format(task_id, status))

    #def run(self, **kwargs):
    def run(self):
        cron_time = 0

        if cron_time:
            print("Runnnn for your life!")
        else:
            raise NotImplementedError()


celery_app.register_task(BackupScheduler())
