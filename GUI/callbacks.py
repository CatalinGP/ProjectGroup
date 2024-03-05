def button1_action():
    from scripts.create.create_manager import VMManagerCreate
    new_box = VMManagerCreate()
    new_box.create_virtual_machine()
    print("Button 1 clicked!")


def button2_action():
    from config.vm_configs import vm_configs_dict
    from scripts.create.clone_vdi import VMClone
    vm_name = vm_configs_dict.get("vm_name")
    new_box = VMClone(vm_name)
    new_box.clone_and_delete_vm()
    print("Button 2 clicked!")


def button3_action():
    print("Button 3 clicked!")

