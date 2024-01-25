import os
import logging
from urllib.request import urlopen
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-live-server-amd64.iso"
filename = "ubuntu-22.04.3-live-server-amd64.iso"
relative_directory = "tmp/downloaded_utils"


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
            logger.info(f"Error: {e}")


check_iso_file(url, filename, relative_directory)