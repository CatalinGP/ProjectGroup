from tkinter import simpledialog, messagebox
from scripts.ssh.ssh_utils import SSHKeyManager


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

    user = simpledialog.askstring("User name", "Enter VM username:")
    if user is None:  # User cancelled the prompt
        messagebox.showwarning("Cancelled", "Operation cancelled.")
        return

    password = simpledialog.askstring("Password", "Enter VM password:", show='*')
    if password is None:  # User cancelled the prompt
        messagebox.showwarning("Cancelled", "Operation cancelled.")
        return

    if ssh_manager.generate_and_copy_key(user, password):
        messagebox.showinfo("Success", "SSH key generated and copied successfully.")
    else:
        messagebox.showerror("Failure", "Failed to copy SSH key.")


def button5_action():
    from tkinter import simpledialog, messagebox
    from scripts.ssh.ssh_utils import SSHKeyManager
    ssh_manager = SSHKeyManager()

    user = simpledialog.askstring("User name", "Enter VM username:")
    if user is None:  # User cancelled the prompt
            messagebox.showwarning("Cancelled", "Operation cancelled.")
            return


    if ssh_manager.transfer_script(user):
            messagebox.showinfo("Success", "SSH key generated and copied successfully.")
    else:
            messagebox.showerror("Failure", "Failed to copy SSH key.")

def button6_action(notebook):
    notebook.select(1)

def button7_action(notebook):
    notebook.select(0)
