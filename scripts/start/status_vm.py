import subprocess
import logging
from config.vm_configs import vm_configs_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CheckVMStatus:
    def __init__(self):
        self.vm_name = vm_configs_dict.get("vm_name")
        self.vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

    def check_virtual_machine_status(self):
        try:
            logger.info(f"Checking status of virtual machine: {self.vm_name}")
            process = subprocess.run([self.vboxmanage_path, "showvminfo", self.vm_name], capture_output=True, text=True)
            output = process.stdout
            if "running (since" in output:
                logger.info("Virtual machine is running.")
            else:
                logger.info("Virtual machine is not running.")
        except FileNotFoundError:
            logger.error(f"Error: VirtualBox executable not found at '{self.vboxmanage_path}'")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error: VirtualBox command failed with return code {e.returncode}")
        except Exception as e:
            logger.error(f"Error checking virtual machine status: {e}")


if __name__ == "__main__":
    checker = CheckVMStatus()
    checker.check_virtual_machine_status()
