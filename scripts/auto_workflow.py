import virtualbox
from config.vm_configs import vm_configs_dict


def get_vm_state(vm_name):
    vbox = virtualbox.VirtualBox()
    try:
        vm = vbox.find_machine(vm_name)
        state = vm.state
        print(f"State of VM '{vm_name}': {state}")
    except virtualbox.library.VBoxError as e:
        print(f"Error: The VM '{vm_name}' cannot be found or VirtualBox not accessible. Details: {e}")

get_vm_state(vm_configs_dict['vm_name'])
