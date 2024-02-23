import os
import logging
from glob import glob
import shutil

from config.vm_configs import vm_configs_dict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VMClone:
    def __init__(self, vm_name):
        self.vm_name = vm_configs_dict.get("vm_name")
        self.vm_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "VirtualMachines", vm_name)
        self.backup_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "backup_VM")

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


if __name__ == "__main__":
    vm_name = vm_configs_dict.get("vm_name")
    vm_backup = VMClone(vm_name)
    vm_backup.clone_vdi()
