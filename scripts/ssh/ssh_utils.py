import paramiko
import os
import scp

<<<<<<< HEAD

def generate_ssh_keypair(key_filename='id_rsa', passphrase=None):
=======
def generate_or_load_ssh_keypair(key_filename='id_rsa', passphrase=None):
>>>>>>> refs/remotes/origin/main
    script_dir = os.path.dirname(os.path.abspath(__file__))
    private_key_path = os.path.join(script_dir, key_filename)
    public_key_path = f'{private_key_path}.pub'

    # Check if the key pair already exists
    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        print(f'SSH key pair already exists:')
    else:
        # Generate an RSA key pair
        key = paramiko.RSAKey.generate(bits=2048)
<<<<<<< HEAD
=======

        # Save the private key
>>>>>>> refs/remotes/origin/main
        key.write_private_key_file(private_key_path, password=passphrase)

        # Save the public key
        with open(public_key_path, 'w', encoding='utf-8') as public_key_file:
            public_key_file.write(f'{key.get_name()} {key.get_base64()}')

        print(f'New SSH key pair generated:')

    return private_key_path, public_key_path

<<<<<<< HEAD

def append_public_key_to_authorized_keys(hostname, username, private_key_path, passphrase=None):
=======
def authenticate_and_copy_key(hostname, username, private_key_path, passphrase=None):
    # Create an SSH client
>>>>>>> refs/remotes/origin/main
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key
        key = paramiko.RSAKey(filename=private_key_path, password=passphrase)

<<<<<<< HEAD
        client.connect(hostname, username=username, pkey=key, port=5050)  # Use the default SSH port (22)

        # Read your public key
        with open(f'{private_key_path}.pub', 'r') as public_key_file:
            public_key = public_key_file.read()
=======
        # Connect to the Ubuntu server
        client.connect(hostname, username=username, pkey=key)

        # Copy the public key to the Ubuntu server
        with client.open_sftp() as sftp:
            sftp.put(public_key_path, f'/home/{username}/.ssh/authorized_keys')
>>>>>>> refs/remotes/origin/main

        # Append your public key to the authorized_keys file
        with client.open_sftp().file(f'/home/{username}/.ssh/authorized_keys', 'a') as authorized_keys_file:
            authorized_keys_file.write(public_key)

        print(f'Public key appended to the authorized_keys file.')

    except paramiko.AuthenticationException as auth_error:
        print(f'Authentication failed: {auth_error}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        # Close the SSH connection
        client.close()

<<<<<<< HEAD

def copy_file_with_scp(hostname, username, private_key_path, source_file, destination_path, passphrase=None):
=======
def ssh_login(hostname, username, private_key_path, passphrase=None):
    # Create an SSH client
>>>>>>> refs/remotes/origin/main
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Load the private key
        key = paramiko.RSAKey(filename=private_key_path, password=passphrase)

<<<<<<< HEAD
        client.connect(hostname, username=username, pkey=key, port=5050)  # Use the default SSH port (22)
=======
        # Connect to the Ubuntu server
        client.connect(hostname, username=username, pkey=key)
>>>>>>> refs/remotes/origin/main

        # Create an SCP client instance using the SSH client
        with scp.SCPClient(client.get_transport()) as scp_client:
            # Copy the source_file to the destination_path on the remote server
            scp_client.put(source_file, destination_path)

        print(f'File copied to the server successfully.')

    except paramiko.AuthenticationException as auth_error:
        print(f'Authentication failed: {auth_error}')
    except scp.SCPException as scp_error:
        print(f'SCP error: {scp_error}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        # Close the SSH connection
        client.close()

if __name__ == "__main__":
<<<<<<< HEAD
    ubuntu_hostname = "127.0.0.1"  # Replace with the actual hostname or IP address of the remote server
    ubuntu_username = "gabriel"  # Replace with the actual username on the remote server
    key_filename = 'id_rsa'  # Adjust if needed
    source_file = 'example.txt'  # Replace with the path to your source file
    destination_path = '/home/gabriel/'  # Replace with the destination path on the remote server
    passphrase = None  # No passphrase for automatic login
=======

    ubuntu_hostname = ssh_config_dict["host"]
    ubuntu_username = ssh_config_dict["user"]
    key_filename = 'id_rsa'
    passphrase = None
>>>>>>> refs/remotes/origin/main

    private_key_path, _ = generate_ssh_keypair(key_filename=key_filename, passphrase=passphrase)

    append_public_key_to_authorized_keys(ubuntu_hostname, ubuntu_username, f'{key_filename}', passphrase)

    copy_file_with_scp(ubuntu_hostname, ubuntu_username, private_key_path, source_file, destination_path, passphrase)
