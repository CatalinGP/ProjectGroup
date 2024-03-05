import tkinter as tk
from tkinter import ttk
from GUI.callbacks import button1_action, button2_action, button3_action
from GUI.vb_box_integration import VirtualBoxPreview


def setup_main_tab(notebook):
    main_tab = ttk.Frame(notebook)
    notebook.add(main_tab, text='Main')

    def _create_vm_with_disabled_button():
        button1.config(state=tk.DISABLED)
        button1_action()
        button1.config(state=tk.NORMAL)

    actions_group = ttk.LabelFrame(main_tab, text='Actions')
    actions_group.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    button1 = tk.Button(actions_group, text="Create from scratch", command=_create_vm_with_disabled_button)
    button1.grid(row=0, column=0, padx=5, pady=5)

    button2 = tk.Button(actions_group, text="Clone VDI", command=button2_action)
    button2.grid(row=0, column=1, padx=5, pady=5)

    button3 = tk.Button(actions_group, text="Create from VDI", command=button3_action)
    button3.grid(row=0, column=2, padx=5, pady=5)

    ios_group = ttk.LabelFrame(main_tab, text='I/O\'s')
    ios_group.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    vm_name_label = tk.Label(ios_group, text="VM Name:")
    vm_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

    vm_name_entry = tk.Entry(ios_group)
    vm_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    disk_size_label = tk.Label(ios_group, text="VM Disk Size:")
    disk_size_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

    disk_size_entry = tk.Entry(ios_group)
    disk_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    cpu_size_label = tk.Label(ios_group, text="VM CPU Size:")
    cpu_size_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

    cpu_size_entry = tk.Entry(ios_group)
    cpu_size_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    timestamp_label = tk.Label(ios_group, text="Timestamp of VM Creation:")
    timestamp_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')

    timestamp_entry = tk.Entry(ios_group)
    timestamp_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')


def setup_config_tab(notebook):
    config_tab = ttk.Frame(notebook)
    notebook.add(config_tab, text='Configuration')

    vm_params_group = ttk.LabelFrame(config_tab, text='VM Parameters Config')
    vm_params_group.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    vm_name_label = tk.Label(vm_params_group, text="VM Name:")
    vm_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

    vm_name_entry = tk.Entry(vm_params_group)
    vm_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    vm_ram_label = tk.Label(vm_params_group, text="VM RAM Size:")
    vm_ram_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

    vm_ram_entry = tk.Entry(vm_params_group)
    vm_ram_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    vm_cpu_label = tk.Label(vm_params_group, text="VM CPU Size:")
    vm_cpu_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

    vm_cpu_entry = tk.Entry(vm_params_group)
    vm_cpu_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    vm_cpu_count_label = tk.Label(vm_params_group, text="VM CPU Count:")
    vm_cpu_count_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')

    vm_cpu_count_entry = tk.Entry(vm_params_group)
    vm_cpu_count_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    # SSH Parameters Config Group Box
    ssh_params_group = ttk.LabelFrame(config_tab, text='SSH Parameters Config')
    ssh_params_group.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    host_label = tk.Label(ssh_params_group, text="Host:")
    host_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

    host_entry = tk.Entry(ssh_params_group)
    host_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    port_label = tk.Label(ssh_params_group, text="Port:")
    port_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

    port_entry = tk.Entry(ssh_params_group)
    port_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    user_label = tk.Label(ssh_params_group, text="User:")
    user_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

    user_entry = tk.Entry(ssh_params_group)
    user_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')


def setup_log_tab(notebook):
    log_tab = ttk.Frame(notebook)
    notebook.add(log_tab, text='Log')


def setup_vm_tab(notebook):
    vm_tab = ttk.Frame(notebook)
    notebook.add(vm_tab, text='Virtual Machine')

    vm_preview_frame = ttk.LabelFrame(vm_tab, text='Virtual Machine Instance Preview')
    vm_preview_frame.pack(padx=10, pady=10, fill='both', expand=True)

    vm_preview_frame.after(3000,
                           lambda: VirtualBoxPreview(vm_preview_frame, 'Virtual Machine'))

