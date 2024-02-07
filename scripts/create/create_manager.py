import os
import logging
import subprocess
import shutil
from urllib.request import urlopen
from config.vm_configs import vm_configs_dict
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-live-server-amd64.iso"
filename = "ubuntu-22.04.3-live-server-amd64.iso"
relative_directory = "tmp/downloaded_utils"
vboxmanage_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"


def check_iso_file(url_path, file_name, rel_directory):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    full_path_dir = os.path.join(script_directory, "..", "..", rel_directory, file_name)

    if os.path.exists(full_path_dir):
        logger.info(f"File '{file_name}' already exists in the specified directory.")
    else:
        try:
            os.makedirs(os.path.join(script_directory, "..", "..", rel_directory), exist_ok=True)
            logger.info(f"Downloading '{file_name}'...")

            with urlopen(url_path) as response, open(full_path_dir, 'wb') as output_file:
                shutil.copyfileobj(response, output_file)

            logger.info(f"File downloaded and saved to {full_path_dir}")
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return None

    return full_path_dir


def create_virtual_machine(iso_path):
    try:
        if iso_path is None:
            logger.error("ISO file path is not valid. Aborting virtual machine creation.")
            return

        vm_name = vm_configs_dict.get("vm_name")
        ram_size = vm_configs_dict.get("ram_size")
        cpu_count = vm_configs_dict.get("cpu_count")
        disk_size = vm_configs_dict.get("disk_size")

        vm_directory = os.path.join(os.path.dirname(__file__), "..", "..", "tmp", "VirtualMachines", vm_name)

        vdi_path = os.path.join("tmp", "VirtualMachines", vm_name, f"{vm_name}.vdi")

        if os.path.exists(vdi_path):
            logger.info("VDI file already exists. Using existing VDI for virtual machine.")
            # code for creating with vdi here....
        else:
            logger.info("VDI file does not exist. Creating new virtual machine...")


        logger.info(f"Creating virtual machine with ISO file: {iso_path}")
        logger.info("Creating virtual machine...")
        subprocess.run([vboxmanage_path, "createvm", "--name", vm_name, "--register", "--basefolder", vm_directory])

        logger.info("Setting VM attributes...")
        subprocess.run([vboxmanage_path, "modifyvm", vm_name, "--memory", str(ram_size)])
        subprocess.run([vboxmanage_path, "modifyvm", vm_name, "--cpus", str(cpu_count)])
        subprocess.run([vboxmanage_path, "modifyvm", vm_name, "--graphicscontroller", "vmsvga"])


        logger.info("Creating storage controllers...")
        subprocess.run([vboxmanage_path, "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata"])
        subprocess.run([vboxmanage_path, "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"])


        # Modify disk name to ensure uniqueness
        vdi_name = f"{vm_name}_{int(time.time())}.vdi"  # Append timestamp to make it unique
        vdi_path = os.path.join(vm_directory, vdi_name)
        logger.info(f"VDI file path: {vdi_path}")


        logger.info("Creating virtual hard disk...")
        vdi_filename = f"{vm_name}.vdi"
        vdi_path = os.path.join(vm_directory, vdi_filename)
        logger.info(f"VDI file path: {vdi_path}")
        subprocess.run([vboxmanage_path, "createhd", "--filename", vdi_path, "--size", str(disk_size)])

        logger.info("Attaching HDD to SATA Controller...")
        subprocess.run([vboxmanage_path, "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", vdi_path])

        logger.info("Attaching ISO to IDE Controller...")
        subprocess.run([vboxmanage_path, "storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_path])
        subprocess.run([vboxmanage_path, "modifyvm", vm_name, "--nic1", "nat", "--natpf1", "ssh,tcp,,22,,22"])

        logger.info("Starting VM...")
        subprocess.run([vboxmanage_path, "startvm", vm_name])

        logger.info("Virtual machine created and started successfully.")

    except Exception as e:
        logger.error(f"Error creating virtual machine: {e}")



iso_path = check_iso_file(url, filename, relative_directory)
create_virtual_machine(iso_path)
