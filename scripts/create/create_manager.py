import os
import logging
import subprocess
import shutil
from urllib.request import urlopen
import time
import random
from config.vm_configs import vm_configs_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VMManagerCreate:
    def __init__(self):
        self.vm_name = vm_configs_dict.get("vm_name")
        self.ram_size = vm_configs_dict.get("ram_size")
        self.cpu_count = vm_configs_dict.get("cpu_count")
        self.disk_size = vm_configs_dict.get("disk_size")
        self.vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
        self.url = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-live-server-amd64.iso"
        self.filename = "ubuntu-22.04.3-live-server-amd64.iso"
        self.relative_directory = "tmp/downloaded_utils"

    def _check_iso_file(self):
        script_directory = os.path.dirname(__file__)
        full_path_dir = os.path.join(script_directory, "..", "..", self.relative_directory, self.filename)

        if os.path.exists(full_path_dir):
            logger.info(f"File '{self.filename}' already exists in the specified directory.")
        else:
            try:
                os.makedirs(os.path.join(script_directory, "..", "..", self.relative_directory), exist_ok=True)
                logger.info(f"Downloading '{self.filename}'...")

                with urlopen(self.url) as response, open(full_path_dir, 'wb') as output_file:
                    shutil.copyfileobj(response, output_file)

                logger.info(f"File downloaded and saved to {full_path_dir}")
            except Exception as e:
                logger.error(f"Error downloading file: {e}")
                return None

        return full_path_dir

    def create_virtual_machine(self):
        try:
            iso_path = self._check_iso_file()
            if iso_path is None:
                logger.error("ISO file path is not valid. Aborting virtual machine creation.")
                return

            vm_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "VirtualMachines", self.vm_name)
            vdi_name = f"{self.vm_name}_{int(time.time())}_{random.randint(0, 1000)}.vdi"
            vdi_path = os.path.join(vm_directory, vdi_name)
            logger.info(f"VDI file path: {vdi_path}")

            if os.path.exists(vdi_path):
                logger.info("VDI file already exists. Using existing VDI for virtual machine.")
            else:
                logger.info("VDI file does not exist. Creating new virtual machine...")

            logger.info(f"Creating virtual machine with ISO file: {iso_path}")
            logger.info("Creating virtual machine...")
            subprocess.run([self.vboxmanage_path, "createvm", "--name", self.vm_name, "--register", "--basefolder",
                            vm_directory])

            logger.info("Setting VM attributes...")
            subprocess.run([self.vboxmanage_path, "modifyvm", self.vm_name, "--memory", str(self.ram_size)])
            subprocess.run([self.vboxmanage_path, "modifyvm", self.vm_name, "--cpus", str(self.cpu_count)])
            subprocess.run([self.vboxmanage_path, "modifyvm", self.vm_name, "--graphicscontroller", "vmsvga"])

            logger.info("Creating storage controllers...")
            subprocess.run([self.vboxmanage_path, "storagectl", self.vm_name, "--name", "SATA Controller", "--add",
                            "sata"])
            subprocess.run([self.vboxmanage_path, "storagectl", self.vm_name, "--name", "IDE Controller", "--add",
                            "ide"])

            logger.info("Creating virtual hard disk...")
            subprocess.run([self.vboxmanage_path, "createhd", "--filename", vdi_path, "--size", str(self.disk_size)])

            logger.info("Attaching HDD to SATA Controller...")
            subprocess.run([self.vboxmanage_path, "storageattach", self.vm_name, "--storagectl", "SATA Controller",
                            "--port", "0", "--device", "0", "--type", "hdd", "--medium", vdi_path])

            logger.info("Attaching ISO to IDE Controller...")
            subprocess.run([self.vboxmanage_path, "storageattach", self.vm_name, "--storagectl", "IDE Controller",
                            "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_path])

            subprocess.run([self.vboxmanage_path, "modifyvm", self.vm_name, "--nic1", "nat", "--natpf1",
                            "ssh,tcp,,22,,22"])

            logger.info("Starting VM...")
            subprocess.run([self.vboxmanage_path, "startvm", self.vm_name])

            logger.info("Virtual machine created and started successfully.")

        except FileNotFoundError as e:
            logger.error(f"Error: VirtualBox executable not found at '{self.vboxmanage_path}'")

        except subprocess.CalledProcessError as e:
            logger.error(f"Error: VirtualBox command failed with return code {e.returncode}")

        except Exception as e:
            logger.error(f"Error creating virtual machine: {e}")

