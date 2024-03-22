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

    title_label = tk.Label(main_tab, text="CyberForge", font=('Arial', 20, 'bold'), fg="#33FFFF", bg="#000000")
    title_label.pack(pady=(25, 40))

    def _create_vm_with_disabled_button():
        button1.config(state=tk.DISABLED)
        button1_action()
        button1.config(state=tk.NORMAL)

    actions_group_style = ttk.Style()
    actions_group_style.configure('DarkGrey.TLabelframe', background='#001F3F', foreground='#00FFFF', font=('Arial', 16, 'bold'))

    actions_group = ttk.LabelFrame(main_tab, style='DarkGrey.TLabelframe')
    actions_group.pack(pady=10)

    button_style = ttk.Style()
    button_style.configure('DarkGrey.TButton', foreground='dark blue')

    button1 = ttk.Button(actions_group, text="New VM", command=_create_vm_with_disabled_button)
    button2 = ttk.Button(actions_group, text="Save VDI", command=button2_action)
    button3 = ttk.Button(actions_group, text="Load VDI", command=button3_action)
    button6 = ttk.Button(actions_group, text="Settings", command=lambda: button6_action(notebook))
    button4 = ttk.Button(actions_group, text="Generate SSH Key", command=button4_action)
    button5 = ttk.Button(actions_group, text="Transfer item", command=button5_action)

    for button in [button1, button2, button3, button4, button5, button6]:
        button.config(width=25, style='DarkGrey.TButton')
        button.pack(side='top', pady=(0, 10), padx=20)

    actions_group.place(relx=0.5, rely=0.5, anchor='center')

@verify_user_guest_or_admin
def setup_config_tab(notebook):
    config_tab = ttk.Frame(notebook)
    notebook.add(config_tab, text='Configuration')

    background_label = tk.Label(config_tab, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    vm_params_group = ttk.LabelFrame(config_tab, text='VM Parameters Config')
    vm_params_group.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    labels_and_entries = [
        ("Name:", tk.Entry(vm_params_group)),
        ("RAM Size (in mb):", tk.Entry(vm_params_group)),
        ("Disk Size (in mb):", tk.Entry(vm_params_group)),
        ("CPU Count:", tk.Entry(vm_params_group))
    ]


    for i, (label_text, entry) in enumerate(labels_and_entries):
        label = tk.Label(vm_params_group, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')


    current_values_frame = ttk.LabelFrame(config_tab, text='Current Values')
    current_values_frame.grid(row=0, column=1, padx=10, pady=10, sticky='w')
    update_current_values(current_values_frame, vm_configs_dict)

    update_button = tk.Button(vm_params_group, text="Update VM Config",
                              command=lambda: update_vm_config(
                                  labels_and_entries[0][1], labels_and_entries[1][1],
                                  labels_and_entries[3][1], labels_and_entries[2][1],
                                  vm_configs_dict, current_values_frame)
                              )
    update_button.grid(row=len(labels_and_entries), column=0, columnspan=2, padx=5, pady=5)

    ssh_params_group = ttk.LabelFrame(config_tab, text='SSH Parameters Config')
    ssh_params_group.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    ssh_labels_and_entries = [
        ("Host:", tk.Entry(ssh_params_group)),
        ("Port:", tk.Entry(ssh_params_group)),
        ("User:", tk.Entry(ssh_params_group))
    ]

    for i, (label_text, entry) in enumerate(ssh_labels_and_entries):
        label = tk.Label(ssh_params_group, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')

    back_button = tk.Button(config_tab, text="Back", command=lambda: button7_action(notebook))
    back_button.grid(row=1, column=2, padx=10, pady=10, sticky='se')

    total_ram_gb, cpu_count, disk_details = get_system_info()
    system_info_group = ttk.LabelFrame(config_tab, text='Windows System Info')
    system_info_group.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    system_info_labels = [
        f"Total RAM: {total_ram_gb:.2f} GB",
        f"CPU Count: {cpu_count}"
    ] + [f"Free space on {mount_point}: {free_space_gb:.2f} GB" for mount_point, free_space_gb in disk_details.items()]

    for info_text in system_info_labels:
        label = tk.Label(system_info_group, text=info_text)
        label.pack()


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

