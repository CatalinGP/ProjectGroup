import subprocess
import logging
from config.vm_configs import vm_configs_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StartVM:
    def __init__(self):
        self.vm_name = vm_configs_dict.get("vm_name")
        self.vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

    def start_virtual_machine(self):
        try:
            logger.info(f"Starting virtual machine: {self.vm_name}")
            subprocess.run([self.vboxmanage_path, "startvm", self.vm_name])
            logger.info("Virtual machine started successfully.")
        except FileNotFoundError as e:
            logger.error(f"Error: VirtualBox executable not found at '{self.vboxmanage_path}'")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error: VirtualBox command failed with return code {e.returncode}")
        except Exception as e:
            logger.error(f"Error starting virtual machine: {e}")
