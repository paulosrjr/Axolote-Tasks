from __future__ import absolute_import, unicode_literals
from time import sleep
import sys
import subprocess

class ScpBackup():
    """
    Execute a SCP Backup
    """
    def __init__(self, **kwargs):
        self.type = "I"
        self.kwargs = kwargs

    def _full_backup(self):
        pass

    def _incremental_backup(self):
        pass

    def _execute_scp_with_key(self):
        pass

    def _execute_scp_with_pass(self):
        pass

    def run(self):
        print("o")
