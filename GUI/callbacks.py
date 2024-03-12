from paramiko import config
from tkinter import simpledialog, messagebox
from scripts.ssh.ssh_utils import SSHKeyManager, transfer_script


def button1_action():
    from scripts.create.create_manager import VMManagerCreate
    new_box = VMManagerCreate()
    new_box.create_virtual_machine()
    print("Creating Virtual Machine!")



def button2_action():
    from config.vm_configs import vm_configs_dict
    from scripts.create.clone_vdi import VMClone
    vm_name = vm_configs_dict.get("vm_name")
    new_box = VMClone(vm_name)
    new_box.clone_and_delete_vm()
    print("VDI cloned and VM unregistered!")


def button3_action():
    from scripts.create.create_from_vdi import VMManagerCreateFromVDI
    new_box = VMManagerCreateFromVDI()
    new_box.create_vm_from_backup_vdi()
    print("Success", "VM created successfully from backup VDI.")

def button4_action():
    from tkinter import simpledialog, messagebox
    from scripts.ssh.ssh_utils import SSHKeyManager
    ssh_manager = SSHKeyManager()


    password = simpledialog.askstring("Password", "Enter VM password:", show='*')
    if password is None:  # User cancelled the prompt
            messagebox.showwarning("Cancelled", "Operation cancelled.")
            return


    if ssh_manager.generate_and_copy_key(password):
            messagebox.showinfo("Success", "SSH key generated and copied successfully.")
    else:
            messagebox.showerror("Failure", "Failed to copy SSH key.")

def button5_action(scripts=None, vm_status=None, ssh_host=None, ssh_port=None, ssh_user=None):
    local_script_path = config.SSHConfigDict
    ssh_key_filepath = config.SSHConfig
    remote_script_path = vm_status.sh

    ssh_manager = SSHKeyManager()
    if not ssh_manager.key_exists(ssh_key_filepath):
        messagebox.showerror("Error", "SSH key does not exist. Please generate and copy the key first.")
        return

    if transfer_script(ssh_key_filepath, ssh_host, ssh_port, ssh_user, local_script_path, remote_script_path):
        messagebox.showinfo("Success", "Script transferred successfully.")
    else:
        messagebox.showerror("Failure", "Failed to transfer script.")
