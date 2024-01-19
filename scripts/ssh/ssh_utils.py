import paramiko
import os
import shutil
from config.ssh_configs import ssh_config_dict


def generate_or_load_ssh_keypair(key_filename='id_rsa', passphrase=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    private_key_path = os.path.join(script_dir, key_filename)
    public_key_path = f'{private_key_path}.pub'

    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        print(f'SSH key pair already exists in the current folder:')
        print(f'Private Key: {private_key_path}')
        print(f'Public Key: {public_key_path}')
    else:
        key = paramiko.RSAKey.generate(bits=2048)

        key.write_private_key_file(private_key_path, password=passphrase)

        with open(public_key_path, 'w', encoding='utf-8') as public_key_file:
            public_key_file.write(f'{key.get_name()} {key.get_base64()}')

        print(f'New SSH key pair generated:')
        print(f'Private Key: {private_key_path}')
        print(f'Public Key: {public_key_path}')

    return private_key_path, public_key_path


def authenticate_and_copy_key(hostname, username, private_key_path, passphrase=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key = paramiko.RSAKey(filename=private_key_path, password=passphrase)

        client.connect(hostname, username=username, pkey=key)

        with client.open_sftp() as sftp:
            sftp.put(public_key_path, f'/home/{username}/.ssh/authorized_keys')

        print(f'Public key copied to the Ubuntu server successfully.')

        # Connect to the Ubuntu server using the private key
        ssh_login(hostname, username, private_key_path, passphrase)

    except Exception as e:
        print(f'Error: {e}')
    finally:
        client.close()


def ssh_login(hostname, username, private_key_path, passphrase=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        key = paramiko.RSAKey(filename=private_key_path, password=passphrase)

        client.connect(hostname, username=username, pkey=key)

    except Exception as e:
        print(f'Error: {e}')
    finally:
        client.close()


if __name__ == "__main__":
    ubuntu_hostname = ssh_config_dict["host"]
    ubuntu_username = ssh_config_dict["user"]
    key_filename = 'id_rsa'  # Adjust if needed
    passphrase = None  # No passphrase for automatic login

    private_key_path, public_key_path = generate_or_load_ssh_keypair(key_filename=key_filename, passphrase=passphrase)
    authenticate_and_copy_key(ubuntu_hostname, ubuntu_username, private_key_path, passphrase)
