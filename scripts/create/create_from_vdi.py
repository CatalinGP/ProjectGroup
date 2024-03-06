import os
import logging
import glob
import subprocess
from config.vm_configs import vm_configs_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VMManagerCreateFromVDI:
    def __init__(self):
        self.vm_name = vm_configs_dict.get("vm_name")
        self.ram_size = vm_configs_dict.get("ram_size")
        self.cpu_count = vm_configs_dict.get("cpu_count")
        self.disk_size = vm_configs_dict.get("disk_size")
        self.vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
        self.backup_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "backup_VM")

    def find_backup_vdi(self):
        vdi_files = glob.glob(os.path.join(self.backup_directory, "*.vdi"))
        if vdi_files:
            return vdi_files[0]  # Use the first VDI found
        logger.info("No VDI found in the backup directory. Consider cloning an existing VM.")
        return None

    def create_vm_from_vdi(self, vdi_path):
        if not vdi_path:
            return

        vm_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "VirtualMachines", self.vm_name)
        os.makedirs(vm_directory, exist_ok=True)

        try:
            logger.info("Creating virtual machine...")
            subprocess.run([self.vboxmanage_path, "createvm", "--name", self.vm_name, "--register", "--basefolder", vm_directory], check=True)

            logger.info("Setting VM attributes...")
            subprocess.run([self.vboxmanage_path, "modifyvm", self.vm_name, "--memory", str(self.ram_size), "--cpus", str(self.cpu_count), "--graphicscontroller", "vmsvga"], check=True)

            logger.info("Creating storage controllers...")
            subprocess.run([self.vboxmanage_path, "storagectl", self.vm_name, "--name", "SATA Controller", "--add", "sata"], check=True)

            logger.info("Attaching HDD to SATA Controller...")
            subprocess.run([self.vboxmanage_path, "storageattach", self.vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", vdi_path], check=True)

            logger.info("VM created successfully with VDI from backup.")
        except subprocess.CalledProcessError as e:
            logger.error(f"VirtualBox command failed: {e}")


    def create_vm_from_backup_vdi(self):
        self.find_backup_vdi()
        self.create_vm_from_vdi(self.find_backup_vdi())


#if __name__ == "__main__":
    #vm_manager = VMManagerCreateFromVDI()
    #backup_vdi_path = vm_manager.find_backup_vdi()
    #if backup_vdi_path:
        #vm_manager.create_vm_from_vdi(backup_vdi_path)
