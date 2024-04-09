from scripts.create.create_manager import VMManagerCreate
from config.vm_configs import vm_configs_dict
from scripts.create.clone_vdi import VMClone
from scripts.create.create_from_vdi import VMManagerCreateFromVDI
from tkinter import messagebox
from scripts.ssh.ssh_utils import SSHKeyManager
from GUI.login_window import create_login_window
from scripts.start.start_vm import StartVM


def button1_action():
    new_box = VMManagerCreate()
    new_box.create_virtual_machine()
    print("Creating Virtual Machine!")


def button2_action():
    vm_name = vm_configs_dict.get("vm_name")
    new_box = VMClone(vm_name)
    if new_box.clone_vdi():
        messagebox.showinfo("Success", "VDI Saved.")
    else:
        messagebox.showerror("Failure", "No VDI file found. Start a new VM first.")


def button3_action():
    vm_name = vm_configs_dict.get("vm_name")
    new_box = VMManagerCreateFromVDI(vm_name)
    if new_box.create_from_vdi():
        messagebox.showinfo("Success", "VDI loaded.")
    else:
        messagebox.showerror("Failure", "Cannot load VDI. No save file found.")


def button4_action():
    ssh_manager = SSHKeyManager()
    login_result = create_login_window(dropdown_users=False, require_password=True)
    user, password = login_result

    if ssh_manager.generate_and_copy_key(user, password):
        messagebox.showinfo("Success", "SSH key generated and copied successfully.")
    else:
        messagebox.showerror("Failure", "Failed to copy SSH key.")


def button5_action():
    ssh_manager = SSHKeyManager()
    login_result = create_login_window(dropdown_users=False, require_password=False)
    user, password = login_result

    if ssh_manager.transfer_script(user):
        messagebox.showinfo("Success", "Script file transferred.")
    else:
        messagebox.showerror("Failure", "SSH error occurred while transferring the script file.")


def button6_action(notebook):
    notebook.select(1)


def button7_action(notebook):
    notebook.select(0)


def button8_action():
    start_vm = StartVM()
    if start_vm.start_virtual_machine():
        messagebox.showinfo("Success", "Loading VM.")
    else:
        messagebox.showerror("Failure", "No VM found. Creating a new one...")
        new_box = VMManagerCreate()
        new_box.create_virtual_machine()
