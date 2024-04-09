import tkinter as tk
from tkinter import messagebox


def update_current_values(current_values_frame, vm_configs_dict, ssh_config_dict):
    for widget in current_values_frame.winfo_children():
        widget.destroy()

    for i, (key, value) in enumerate(vm_configs_dict.items()):
        label = tk.Label(current_values_frame, text=f"{key}: {value}")
        label.grid(row=i, column=0, padx=5, pady=2, sticky="w")

    for j, (key, value) in enumerate(ssh_config_dict.items(), start=i + 1):
        label = tk.Label(current_values_frame, text=f"{key}: {value}")
        label.grid(row=j, column=0, padx=5, pady=2, sticky="w")


def update_vm_config(vm_name_entry,
                     vm_ram_entry,
                     vm_cpu_count_entry,
                     disk_size_entry,
                     host_entry,
                     port_entry,
                     vm_configs_dict,
                     ssh_config_dict,
                     current_values_frame):

    vm_configs_dict["vm_name"] = vm_name_entry.get() or vm_configs_dict["vm_name"]
    vm_configs_dict["ram_size"] = int(vm_ram_entry.get()) if vm_ram_entry.get() else vm_configs_dict["ram_size"]
    vm_configs_dict["cpu_count"] = int(vm_cpu_count_entry.get()) \
        if vm_cpu_count_entry.get() else vm_configs_dict["cpu_count"]
    vm_configs_dict["disk_size"] = int(disk_size_entry.get()) if disk_size_entry.get() else vm_configs_dict["disk_size"]
    ssh_config_dict["host"] = int(host_entry.get()) if host_entry.get() else ssh_config_dict["host"]
    ssh_config_dict["port"] = int(port_entry.get()) if port_entry.get() else ssh_config_dict["port"]
    update_current_values(current_values_frame, vm_configs_dict, ssh_config_dict)
    messagebox.showinfo("Changes Saved", "Settings has been updated successfully.")
