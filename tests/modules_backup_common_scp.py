import sys
import os
import unittest
import mock
from unittest.mock import MagicMock, MagicProxy, Mock, PropertyMock, patch, create_autospec
from modules.backup.common.scp import ScpBackup
import subprocess


class ScpBackupTestCase(unittest.TestCase):

    def setUp(self):
        self.scp_with_key = {
            "scp_type": "key",
            "key": "/home/{}/.ssh/key".format(os.getenv('USER_TEST', 'travis')),
            "password": "",
            "parameters": "-r -o IdentitiesOnly=yes",
            "username": "{}".format(os.getenv('USER_TEST', 'travis')),
            "host": "localhost",
            "remotepath": "/home/{}/.ssh".format(os.getenv('USER_TEST', 'travis')),
            "localpath": "/tmp/scp_test"
        }
        self.scp_with_password = {
            "scp_type": "password",
            "key": "",
            "password": "password",
            "parameters": "-r -o IdentitiesOnly=yes",
            "username": "{}".format(os.getenv('USER_TEST', 'travis')),
            "host": "localhost",
            "remotepath": "/home/{}/.ssh".format(os.getenv('USER_TEST', 'travis')),
            "localpath": "/tmp/scp_test"
        }
        self.mock = Mock()

    def test_run_with_key(self):
        scp_backup = ScpBackup(**self.scp_with_key)
        scp_backup._execute_scp_with_key = MagicMock(return_value={'code': "0", 'out': "done", 'status': True})
        result = scp_backup.run()
        self.assertEqual(result['code'], '0')
        self.assertTrue(result['status'])
        self.assertEqual(scp_backup.host, 'localhost')
        self.assertEqual(scp_backup.password, '')
        self.assertEqual(scp_backup.scp_type, 'key')
        self.assertEqual(scp_backup.key, "/home/{}/.ssh/key".format(os.getenv('USER_TEST', 'travis')))

    def test_run_with_password(self):
        scp_backup = ScpBackup(**self.scp_with_password)
        scp_backup._execute_scp_with_pass = MagicMock(return_value={'code': "0", 'out': "done", 'status': True})
        result = scp_backup.run()
        self.assertEqual(result['code'], '0')
        self.assertTrue(result['status'])
        self.assertEqual(scp_backup.host, 'localhost')
        self.assertEqual(scp_backup.password, 'password')
        self.assertEqual(scp_backup.scp_type, 'password')
        self.assertEqual(scp_backup.key, '')

    def test_run_with_error(self):
        scp_backup = ScpBackup()
        result = scp_backup.run()
        self.assertFalse(result['status'])

    @mock.patch('subprocess.Popen.communicate', return_value=('stout', 'stderr'))
    @mock.patch('subprocess.Popen.wait', return_value=0)
    @mock.patch('subprocess.Popen.poll', return_value=0)
    def test_execution_with_key(self, m1, m2, m3):
        scp_backup = ScpBackup(**self.scp_with_key)
        subprocess.Popen.returncode = MagicMock(return_value=0)
        scp_backup._execute_scp_with_key = MagicMock(return_value={'code': '0', 'out': '[]', 'status': True})
        self.assertEqual(scp_backup._execute_scp_with_key(), {'code': '0', 'out': '[]', 'status': True})

    @mock.patch('subprocess.Popen.poll', return_value=0)
    @mock.patch('subprocess.Popen.communicate', return_value=('stout', 'stderr'))
    @mock.patch('subprocess.Popen.wait', return_value=0)
    def test_execution_with_password(self, m1, m2, m3):
        command = "sshpass -p 'test' scp -o stricthostkeychecking=no -rC -P 22 backup@localhost:/tmp/files /tmp/backup"
        scp_backup = ScpBackup(**self.scp_with_password)
        subprocess.Popen.returncode = MagicMock(return_value=0)
        mock.patch.object('scp_backup._execute_scp_with_pass', 'command', new=command)
        scp_backup._execute_scp_with_pass = MagicMock(return_value={'code': '0', 'out': '[]', 'status': True})
        
        self.assertEqual(scp_backup._execute_scp_with_pass(), {'code': '0', 'out': '[]', 'status': True})
