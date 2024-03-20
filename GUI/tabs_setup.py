import tkinter as tk
from tkinter import ttk
from GUI.callbacks import button1_action, button2_action, button3_action, button4_action, button5_action, button6_action, button7_action
from GUI.vb_box_integration import VirtualBoxPreview
from config.system_info import get_system_info
from config.vm_configs import vm_configs_dict
from config.update_vm_config import update_current_values, update_vm_config
from tkinter import PhotoImage

def setup_main_tab(notebook):
    global background_image

    notebook_width = 800
    notebook_height = 500
    notebook.config(width=notebook_width, height=notebook_height)

    main_tab = ttk.Frame(notebook)
    notebook.add(main_tab, text='Main')

    background_image = PhotoImage(file="media/background_image.PNG")


    background_label = tk.Label(main_tab, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(main_tab, text="Placeholder", font=('Arial', 20, 'bold'), fg="#33FFFF", bg="#000000")
    title_label.pack(pady=(25, 40))

    def _create_vm_with_disabled_button():
        button1.config(state=tk.DISABLED)
        button1_action()
        button1.config(state=tk.NORMAL)

    actions_group_style = ttk.Style()
    actions_group_style.configure('DarkGrey.TLabelframe', background='#001F3F', foreground='#00FFFF', font=('Arial', 16, 'bold'))


    button_style = ttk.Style()
    button_style.configure('DarkGrey.TButton', foreground='dark blue')

    actions_group = ttk.LabelFrame(main_tab, style='DarkGrey.TLabelframe')
    actions_group.pack(pady=10)


    button1 = ttk.Button(actions_group, text="New VM", command=_create_vm_with_disabled_button)
    button2 = ttk.Button(actions_group, text="Save VDI", command=button2_action)
    button3 = ttk.Button(actions_group, text="Load VDI", command=button3_action)
    button6 = ttk.Button(actions_group, text="Settings", command=lambda: button6_action(notebook))
    button4 = ttk.Button(actions_group, text="Create & Copy SSH Key", command=button4_action)
    button5 = ttk.Button(actions_group, text="Transfer script", command=button5_action)


    for button in [button1, button2, button3, button4, button5, button6]:
        button.config(width=25, style='DarkGrey.TButton')
        button.pack(side='top', pady=(0, 10), padx=20)

    actions_group.place(relx=0.5, rely=0.5, anchor='center')



def setup_config_tab(notebook):

    config_tab = ttk.Frame(notebook)
    notebook.add(config_tab, text='Configuration')

    background_label = tk.Label(config_tab, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    vm_params_group = ttk.LabelFrame(config_tab, text='VM Parameters Config')
    vm_params_group.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    vm_name_label = tk.Label(vm_params_group, text="Name:")
    vm_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

    vm_name_entry = tk.Entry(vm_params_group)
    vm_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    vm_ram_label = tk.Label(vm_params_group, text="RAM Size (in mb):")
    vm_ram_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

    vm_ram_entry = tk.Entry(vm_params_group)
    vm_ram_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    vm_cpu_count_label = tk.Label(vm_params_group, text="CPU Count:")
    vm_cpu_count_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')

    vm_cpu_count_entry = tk.Entry(vm_params_group)
    vm_cpu_count_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    disk_size_label = tk.Label(vm_params_group, text="Disk Size (in mb):")
    disk_size_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

    disk_size_entry = tk.Entry(vm_params_group)
    disk_size_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    current_values_frame = ttk.LabelFrame(config_tab, text='Current Values')
    current_values_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    update_current_values(current_values_frame, vm_configs_dict)

    update_button = tk.Button(vm_params_group, text="Update VM Config",
                              command=lambda: update_vm_config(vm_name_entry, vm_ram_entry, vm_cpu_count_entry,
                                                               disk_size_entry, vm_configs_dict, current_values_frame))
    update_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

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

    back_button = tk.Button(config_tab, text="Back", command=lambda: button7_action(notebook))
    back_button.grid(row=1, column=2, padx=10, pady=10, sticky='se')

    #system info

    total_ram_gb, cpu_count, disk_details = get_system_info()
    system_info_group = ttk.LabelFrame(config_tab, text='Windows System Info')
    system_info_group.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    ram_label = tk.Label(system_info_group, text=f"Total RAM: {total_ram_gb:.2f} GB")
    ram_label.pack()


    cpu_label = tk.Label(system_info_group, text=f"CPU Count: {cpu_count}")
    cpu_label.pack()

    for mount_point, free_space_gb in disk_details.items():
        disk_label = tk.Label(system_info_group, text=f"Free space on {mount_point}: {free_space_gb:.2f} GB")
        disk_label.pack()

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
