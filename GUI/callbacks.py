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
