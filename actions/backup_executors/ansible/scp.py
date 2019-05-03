from __future__ import absolute_import, unicode_literals
from time import sleep
import sys
import subprocess
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
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


class AnsibleScp(celery_app.Task):
    """
    Execute a SCP Backup
    """
    def __init__(self):
        self.name = "actions.backup_executors.ansible.scp"
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

        # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
        options = Options(connection='local', module_path=['/to/mymodules'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)

        # initialize needed objects
        loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
        passwords = dict(vault_pass='secret')

        # Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
        results_callback = ResultCallback()

        # create inventory, use path to host config file as source or hosts in a comma separated string
        inventory = InventoryManager(loader=loader, sources='localhost,')

        # variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        # create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.
        play_source =  dict(
                name = ip,
                hosts = ip,
                gather_facts = 'no',
                tasks = [
                    dict(action=dict(module='shell', args='ls -lash'), register='shell_out_ls'),
                    dict(action=dict(module='debug', args=dict(msg='{{shell_out_ls.stdout}}'))),
                 ]
            )

        # Create play object, playbook objects use .load instead of init or new methods,
        # this will also automatically create the task objects from the info provided in play_source
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      options=options,
                      passwords=passwords,
                      stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                  )
            result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
        finally:
            # we always need to cleanup child procs and the structres we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

celery_app.register_task(AnsibleScp())
