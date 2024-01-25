import os
from urllib.request import urlopen
import shutil

url = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-live-server-amd64.iso"
filename = "ubuntu-22.04.3-live-server-amd64.iso"
relative_directory = "tmp/downloaded_utils"


def check_iso_file(url, filename, relative_directory):
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine the script directory, move up two levels, enter the relative directory, and append the filename
    full_path_dir = os.path.join(script_directory, "..", "..", relative_directory, filename)

    # Check if the file already exists
    if os.path.exists(full_path_dir):
        print(f"File '{filename}' already exists in the specified directory.")
    else:
        try:
            # Ensure the necessary directory structure exists
            os.makedirs(os.path.join(script_directory, "..", "..", relative_directory), exist_ok=True)

            print(f"Downloading '{filename}'...")

            # Download the file using urllib and shutil
            with urlopen(url) as response, open(full_path_dir, 'wb') as output_file:
                shutil.copyfileobj(response, output_file)

            print(f"File downloaded and saved to {full_path_dir}")
        except Exception as e:
            print(f"Error: {e}")

check_iso_file(url, filename, relative_directory)