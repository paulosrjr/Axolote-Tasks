from __future__ import absolute_import, unicode_literals
from time import sleep
import sys
import subprocess
from actions import celery_app, logger, test_none

class Scp(celery_app.Task):
    """
    Execute a SCP Backup
    """
    def __init__(self):
        self.name = "actions.backup_executors.scp"
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
        scp_type = kwargs.get('scp_type')
        key = kwargs.get('key')
        password = kwargs.get('password')
        parameters = kwargs.get('parameters')
        username = kwargs.get('username')
        ip = kwargs.get('ip')
        remotepath = kwargs.get('remotepath')
        localpath = kwargs.get('localpath')

        if scp_type == "password":
            command = "sshpass -p '{}' scp -o stricthostkeychecking=no {} {}@{}:{} {}".format(
                password,
                parameters,
                username,
                ip,
                remotepath,
                localpath)
            log = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
            self.message = log.returncode
            return self.message

        elif scp_type == "key":
            command = "scp -i {} -o stricthostkeychecking=no {} {}@{}:{} {}".format(
                key,
                parameters,
                username,
                ip,
                remotepath,
                localpath)
            log = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE)
            self.message = log.returncode
            return self.message

        else:
            raise NotImplementedError()

celery_app.register_task(Scp())
