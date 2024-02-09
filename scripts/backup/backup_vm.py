import os
import paramiko
from tkinter import simpledialog


class VMBackupManager:
    def __init__(self, vm_name, vm_ip, vm_username, vm_password):
        self.vm_name = vm_name
        self.vm_ip = vm_ip
        self.vm_username = vm_username
        self.vm_password = vm_password

    def _backup_file_path(self):
        return f"{self.vm_name}.vdi"

    def _verify_backup_exists(self):
        backup_file = self._backup_file_path()
        return os.path.exists(backup_file)

    def create_automated_backup(self, source_path, destination_path):
        if self._verify_backup_exists():
            print(f"Automated backup for {self.vm_name} already exists.")
        else:
            print(f"Creating automated backup for {self.vm_name}.")
            self._backup_file(source_path, destination_path)

    def create_manual_backup(self):
        if self._verify_backup_exists():
            print(f"Manual backup for {self.vm_name} already exists.")
        else:
            print(f"Creating manual backup for {self.vm_name}.")
            source_path = input("Enter the source file path on the VM: ")
            destination_path = input("Enter the destination file path on Windows: ")
            self._backup_file(source_path, destination_path)

    def _backup_file(self, source_path, destination_path):
        scp = None  # Initialize scp outside the try block

        try:
            # Establish SSH connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.vm_ip, username=self.vm_username, password=self.vm_password)

            # Create an SCP client
            scp = ssh.open_sftp()

            # Transfer files from VM to Windows
            scp.get(source_path, destination_path)

            print(f"Backup successful. File transferred from {source_path} to {destination_path}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the connections
            if scp:
                scp.close()
            if ssh:
                ssh.close()


# Get VM details from user input

vm_name = simpledialog.askstring("Enter VM Name", "Enter the VM name:")
vm_ip = simpledialog.askstring("Enter VM IP", "Enter the VM IP address:")
vm_username = simpledialog.askstring("Enter VM Username", "Enter the VM username:")
vm_password = simpledialog.askstring("Enter VM Password", "Enter the VM password:")

# Create VMBackupManager instance
vm_backup_manager = VMBackupManager(vm_name, vm_ip, vm_username, vm_password)

# Choose backup type
backup_type = simpledialog.askstring("Choose Backup Type", "Enter 'automated' or 'manual' for backup type:")
if backup_type.lower() == 'automated':
    vm_backup_manager.create_automated_backup(source_path="important_files.sh", destination_path="Desktop")
elif backup_type.lower() == 'manual':
    vm_backup_manager.create_manual_backup()
else:
    print("Invalid backup type. Please enter 'automated' or 'manual'.")
