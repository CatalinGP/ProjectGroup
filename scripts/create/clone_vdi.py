import os
import logging
from glob import glob
import shutil
import subprocess

from config.vm_configs import vm_configs_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VMClone:
    def __init__(self, vm_name):
        self.vm_name = vm_name
        self.vm_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "VirtualMachines", vm_name)
        self.backup_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "backup_VM")
        self.vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
        print(f"Looking for VDI in: {self.vm_directory}")

    def clone_vdi(self):
        os.makedirs(self.backup_directory, exist_ok=True)

        vdi_files = glob(os.path.join(self.vm_directory, "*.vdi"))
        if not vdi_files:
            logger.info("No VDI file found. Create a VM first.")
            return

        for vdi_path in vdi_files:
            try:
                backup_vdi_path = os.path.join(self.backup_directory, os.path.basename(vdi_path))

                shutil.copy2(vdi_path, backup_vdi_path)
                logger.info(f"VDI file '{vdi_path}' cloned to '{backup_vdi_path}'")
            except Exception as e:
                logger.error(f"Error cloning VDI file: {e}")

    def delete_vm_folder(self):

        try:
            # Unregister and delete VM from VirtualBox
            subprocess.run([self.vboxmanage_path, "unregistervm", self.vm_name, "--delete"], check=True)
            logger.info(f"VM '{self.vm_name}' unregistered and all associated files deleted.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to unregister and delete VM '{self.vm_name}': {e}")
            return

        if os.path.exists(self.vm_directory):
            try:
                shutil.rmtree(self.vm_directory)
                logger.info(f"VM folder '{self.vm_directory}' has been successfully deleted.")
            except Exception as e:
                logger.error(f"Error deleting VM folder: {e}")
        else:
            logger.info("VM folder does not exist or has already been deleted.")


    def clone_and_delete_vm(self):
        self.clone_vdi()
        self.delete_vm_folder()


# if __name__ == "__main__":
#     vm_name = vm_configs_dict.get("vm_name", "DefaultVMName")
#     vm_clone = VMClone(vm_name)
#     vm_clone.clone_vdi()
#     vm_clone.delete_vm_folder()
