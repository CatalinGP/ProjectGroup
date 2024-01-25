import subprocess
import os
import sys
import logging
from paramiko.ssh_exception import AuthenticationException
from paramiko import SSHClient, AutoAddPolicy, RSAKey, SSHException
from scp import SCPClient
# from config.GUI_input import provide_input

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

status_script_filename = "vm_status.sh"


def create_ssh_key(ssh_key_path):
    ssh_dir = os.path.dirname(ssh_key_path)
    if not os.path.exists(ssh_dir):
        logger.info(f"Creating directory {ssh_dir}")
        os.makedirs(ssh_dir, exist_ok=True)

    if not os.path.exists(ssh_key_path):
        logger.info("Generating SSH key...")
        try:
            subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-N", "", "-f", ssh_key_path], check=True)
            logger.info(f"SSH key generated at {ssh_key_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate SSH key: {e}")
            sys.exit(1)
    else:
        logger.info(f"SSH key already exists at {ssh_key_path}")


def is_vm_reachable(ssh_host):
    try:
        response = subprocess.run(['ping', '-n', '1', ssh_host],
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
        return response.returncode == 0
    except subprocess.SubprocessError:
        return False


def copy_public_key_to_vm(ssh_host, ssh_port, ssh_user, local_public_key_path, ssh_key_filepath, password):
    try:
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())

            try:
                ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
                ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)
            except AuthenticationException as key_auth_error:
                logger.warning(f"SSH key-based authentication failed: {key_auth_error}")

            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, password=password)

            with open(local_public_key_path, 'r') as local_public_key_file:
                public_key = local_public_key_file.read()

            ssh_client.exec_command(f'echo "{public_key}" >> ~/.ssh/authorized_keys')

            return True

    except SSHException as e:
        logger.error(f"SSH error while copying public key to VM: {e}")
    except Exception as e:
        logger.error(f"An error occurred while connecting to VM: {e}")

    return False


def transfer_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user, local_status_script_path, remote_script_path):
    try:
        ssh_key = RSAKey.from_private_key_file(ssh_key_filepath)
        with SSHClient() as ssh_client:
            ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, pkey=ssh_key)
            with SCPClient(ssh_client.get_transport()) as scp_client:
                scp_client.put(local_status_script_path, remote_script_path)

                ssh_client.exec_command(f'chmod +x {status_script_filename}')

        logger.info(f"SCP: File transferred successfully")
        return True
    except SSHException as e:
        logger.error(f"SSH error while transferring script: {e}")
        return False


