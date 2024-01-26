import os
import config.GUI_input
from tkinter import simpledialog

class VMBackupManager:
    def __init__(self, vm_name):
        self.vm_name = vm_name

    def _backup_file_path(self):
        return f"{self.vm_name}.vdi"

    def _verify_backup_exists(self):
        backup_file = self._backup_file_path()
        return os.path.exists(backup_file)

    def create_automated_backup(self):
        if self._verify_backup_exists():
            print(f"Automated backup for {self.vm_name} already exists.")
        else:
            print(f"Creating automated backup for {self.vm_name}.")

    def create_manual_backup(self):
        if self._verify_backup_exists():
            print(f"Manual backup for {self.vm_name} already exists.")
        else:
            print(f"Creating manual backup for {self.vm_name}.")

# Define title and prompt before using them
title = "Enter User Input"
prompt = "Enter your input:"
user_input = simpledialog.askstring(title, prompt, show='~')


#vm_backup_manager = VMBackupManager("your_vm_name")

#user_input = simpledialog.askstring(title, prompt, show='~')

# backup_choice = input("Choose backup type (automated/manual): ").lower()
#
# if backup_choice == "automated":
#     vm_backup_manager.create_automated_backup()
# elif backup_choice == "manual":
#     vm_backup_manager.create_manual_backup()
# else:
#     print("Invalid choice. Please choose either 'automated' or 'manual'.")
