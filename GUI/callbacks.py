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

    from GUI.login_window import create_login_window
    login_result = create_login_window(dropdown_users=False, require_password=True)
    user, password = login_result

    if ssh_manager.generate_and_copy_key(user, password):
        messagebox.showinfo("Success", "SSH key generated and copied successfully.")
    else:
        messagebox.showerror("Failure", "Failed to copy SSH key.")


def button5_action():
    from tkinter import messagebox
    from scripts.ssh.ssh_utils import SSHKeyManager
    ssh_manager = SSHKeyManager()

    from GUI.login_window import create_login_window

    login_result = create_login_window(dropdown_users=False, require_password=False)
    user, password = login_result

    if ssh_manager.transfer_script(user):
        messagebox.showinfo("Success", "SSH key generated and copied successfully.")
    else:
        messagebox.showerror("Failure", "Failed to copy SSH key.")


def button6_action(notebook):
    notebook.select(1)


def button7_action(notebook):
    notebook.select(0)

