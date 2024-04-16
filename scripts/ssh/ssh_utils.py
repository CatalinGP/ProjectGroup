import subprocess
import os
import logging

from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException
from paramiko import SSHClient, AutoAddPolicy, SSHException
from scp import SCPClient
from config.ssh_configs import ssh_config_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SSHKeyManager:
    def __init__(self, relative_path='config/ssh_keys', key_name="id_rsa"):
        base_dir = os.path.join(os.path.dirname(__file__), "..", "..")
        self.folder_path = os.path.abspath(os.path.join(base_dir, relative_path))
        self.key_name = key_name
        self.ssh_key_path = os.path.join(self.folder_path, key_name)
        self.ssh_host = ssh_config_dict.get("host")
        self.ssh_port = ssh_config_dict.get("port")

    def is_vm_reachable(self):
        try:
            response = subprocess.run(['ping', '-n', '1', self.ssh_host],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
            return response.returncode == 0
        except subprocess.SubprocessError:
            return False

    def generate_and_copy_key(self, user, password):

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            logger.info(f"Created directory: {self.folder_path}")

        if not os.path.exists(self.ssh_key_path):
            logger.info("Generating SSH key...")
            try:
                subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-N", "", "-f",
                                self.ssh_key_path],
                               check=True)
                logger.info(f"SSH key generated at {self.ssh_key_path}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to generate SSH key: {e}")
                return False
        else:
            logger.info("SSH key already exists.")

        if not self.is_vm_reachable():
            logger.error(f"VM {self.ssh_host} is not reachable.")
            return False

        public_key_path = f"{self.ssh_key_path}.pub"
        try:
            with SSHClient() as ssh:
                ssh.set_missing_host_key_policy(AutoAddPolicy())
                ssh.connect(self.ssh_host, port=self.ssh_port, username=user, password=password)

                with SCPClient(ssh.get_transport()) as scp:
                    target_path = f'/home/{user}/.ssh/authorized_keys'
                    scp.put(public_key_path, target_path)
                    logger.info(f"Successfully copied the SSH public key to {self.ssh_host}:{target_path}")

                return True
        except AuthenticationException:
            logger.error("Authentication failed.")
        except SSHException as e:
            logger.error(f"SSH error occurred: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        return False

    def transfer_script(self, user):
        try:
            remote_script_path = f'/home/{user}'
            with SSHClient() as ssh_client:
                ssh_client.set_missing_host_key_policy(AutoAddPolicy())
                ssh_key = RSAKey.from_private_key_file(self.ssh_key_path)
                ssh_client.connect(hostname=self.ssh_host,
                                   port=self.ssh_port,
                                   username=user,
                                   pkey=ssh_key)
                base_dir = os.path.join(os.path.dirname(__file__))
                transfer_script = "vm_status.sh"
                target_one_level_upper = os.path.abspath(os.path.join(base_dir, os.pardir))
                local_status_script_path = os.path.join(target_one_level_upper, "transfer_to", transfer_script)
                with SCPClient(ssh_client.get_transport()) as scp_client:
                    scp_client.put(local_status_script_path, remote_script_path)
                stdin, stdout, stderr = ssh_client.exec_command(f'chmod +x {remote_script_path}')
                if stderr.read():
                    raise SSHException("Error setting execute permission on remote script.")
                logger.info("File transferred and permissions set successfully.")
                return True
        except SSHException:
            logger.error("SSH error occurred while transferring the script.")
            return False
        except Exception as e:
            logger.error(f"Unexpected error occurred during script transfer: {str(e)}")
            return False

    def get_remote_ip(self, user):
        """
        Retrieves the IP address of the remote machine.
        """
        try:
            with SSHClient() as ssh_client:
                ssh_client.set_missing_host_key_policy(AutoAddPolicy())
                ssh_key = RSAKey.from_private_key_file(self.ssh_key_path)
                ssh_client.connect(hostname=self.ssh_host,
                                   port=self.ssh_port,
                                   username=user,
                                   pkey=ssh_key,
                                   look_for_keys=True,
                                   allow_agent=False)

                stdin, stdout, stderr = ssh_client.exec_command(
                    "ip addr | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d'/' -f1")
                ip_addresses = stdout.read().decode().strip().split('\n')
                ip_addresses = [ip for ip in ip_addresses if ip]

                for ip in ip_addresses:
                    logger.info(f"Found IP address: {ip}")

                return ip_addresses[0]

        except SSHException as e:
            logger.error(f"SSH error occurred while trying to retrieve IP address: {e}")
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

        return None
