from __future__ import absolute_import, unicode_literals
from actions import celery_app
from modules.backup.common.scp import ScpBackup, exceptions


class Scp(celery_app.Task):
    """
    Execute a async SCP Backup
    """
    def __init__(self):
        self.name = "actions.backup_executors.common.scp"
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
        scp_backup = ScpBackup(**kwargs)
        print("Async SCP backup")
        result = scp_backup.run()
        print(result)
        if not result or result["status"] is False:
            print("Job is failed")
            self.message = result
            raise exceptions.BackupExecutionError()
        else:
            print("Job is done")
            self.message = result
            return True


celery_app.register_task(Scp())
