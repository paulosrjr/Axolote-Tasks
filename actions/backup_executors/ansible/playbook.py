from __future__ import absolute_import, unicode_literals
from time import sleep
import sys
import subprocess
import json
import shutil
from collections import namedtuple
from ansible.playbook import Playbook
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
from actions import celery_app, logger, test_none


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


class AnsiblePlaybook(celery_app.Task):
    """
    Execute a Ansible Playbook Backup
    """
    def __init__(self):
        self.name = "actions.backup_executors.ansible.playbook"
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
        playbook_file = kwargs.get('playbook_file')
        pb = Playbook(playbook=playbook_file)
        pb.run()

celery_app.register_task(AnsiblePlaybook())
