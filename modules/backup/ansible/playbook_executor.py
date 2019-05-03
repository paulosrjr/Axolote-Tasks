from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor


class AnsiblePlaybookExecutor():

    def __init__(self):

        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=['PATH'])
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}

        passwords={}

        Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'sudo_user',
                              'sudo',
                              'diff'])
        options = Options(connection='smart',
                               remote_user=None,
                               ack_pass=None,
                               sudo_user=None,
                               forks=5,
                               sudo=None,
                               ask_sudo_pass=False,
                               verbosity=5,
                               module_path=None,
                               become=None,
                               become_method=None,
                               become_user=None,
                               check=False,
                               diff=False,
                               listhosts=None,
                               listtasks=None,
                               listtags=None,
                               syntax=None)

        playbook = PlaybookExecutor(playbooks=['/home/felixc/dev/ansible-playbook/test/test001_api_pb.yaml'],inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,options=options,passwords=passwords)
        playbook.run()