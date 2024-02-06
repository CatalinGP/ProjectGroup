import unittest
import paramiko

SSH_HOST = '127.0.0.1'
SSH_PORT = 5050
SSH_USER = 'gabriel'
SSH_KEY_PATH = 'id_rsa'


class TestSSHConnection(unittest.TestCase):
    def setUp(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def test_ssh_connection(self):
        try:
            self.ssh_client.connect(hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, key_filename=SSH_KEY_PATH)
        except Exception as e:
            self.fail(f"SSH connection failed: {e}")
        else:
            print("SSH connection successful.")
        finally:
            self.ssh_client.close()

    def tearDown(self):
        if self.ssh_client:
            self.ssh_client.close()


if __name__ == '__main__':
    unittest.main()
