from __future__ import absolute_import, unicode_literals
import subprocess
from modules.backup.common.scp import exceptions


class ScpBackup:
    """
    Execute a SCP Backup
    """

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.backup_type = self._kwargs.get('backup_type', 'F')
        self.storage_type = self._kwargs.get('storage_type', 'local')
        self.scp_type = self._kwargs.get('scp_type', 'password')
        self.key = self._kwargs.get('key', '')
        self.password = self._kwargs.get('password', 'backup')
        self.parameters = self._kwargs.get('parameters', '-rC')
        self.username = self._kwargs.get('username', 'backup')
        self.host = self._kwargs.get('host', 'localhost')
        self.port = self._kwargs.get('port', '22')
        self.remote_path = self._kwargs.get('remote_path', '/backup')
        self.local_path = self._kwargs.get('local_path', '/home')
        self._result = ""
        self._message = ""
        self._pipe = subprocess.PIPE

    def _message_return(self, log):
        if log.returncode != 0:
            situation_message = {'code': "{}".format(log.returncode),
                                 'out': "{}".format(str(log.stdout.readlines())),
                                 # "args": "{}".format(str(log.args)),
                                 'status': False}
            self._message = situation_message
            print(self._message)
            return self._message
        else:
            situation_message = {'code': "{}".format(log.returncode),
                                 'out': "{}".format(str(log.stdout.readlines())),
                                 'status': True}
            self._message = situation_message
            return self._message

    def _save_key(self):
        pass

    def _get_password(self):
        pass

    def _check_sshpass(self):
        print("Check if sshpass exist")
        command = "sshpass"
        log = subprocess.Popen(command, shell=True, stdout=self._pipe, stderr=subprocess.STDOUT)
        log.wait()
        return True if int(log.returncode) == 0 else False

    def _execute_scp_with_key(self):
        print("Try SCP with key")
        command = "scp -i {} -o stricthostkeychecking=no {} {}@{}:{} {}".format(
            self.key,
            self.parameters,
            self.username,
            self.host,
            self.remote_path,
            self.local_path)
        log = subprocess.Popen(command, bufsize=2048, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, close_fds=True)
        log.wait()
        log_result = self._message_return(log)
        return log_result

    def _execute_scp_with_pass(self):
        print("Try SCP with password")
        if self._check_sshpass():
            command = "sshpass -p '{}' scp -o stricthostkeychecking=no {} -P {} {}@{}:{} {}".format(
                    self.password,
                    self.parameters,
                    self.port,
                    self.username,
                    self.host,
                    self.remote_path,
                    self.local_path)
            print(command)
            log = subprocess.Popen(command, bufsize=2048, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, close_fds=True)
            log.wait()
            log_result = self._message_return(log)
            return log_result
        else:
            self._result = "sshpass not found {}".format(self.scp_type)
            return {'message': "".format(self._result), 'status': False}

    def run(self):
        print("Running SCP backup")
        # print(self._kwargs)
        if self.scp_type == "password":
            self._result = self._execute_scp_with_pass()
            return self._result
        elif self.scp_type == "key":
            self._result = self._execute_scp_with_key()
            return self._result
        else:
            print("Error in SCP type choice")
            self._result = "scp type not found {}".format(self.scp_type)
            return {'message': "".format(self._result), 'status': False}
