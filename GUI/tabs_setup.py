import tkinter as tk
from tkinter import ttk
from GUI.callbacks import button1_action, button2_action, button3_action, button4_action, button5_action, button6_action, button7_action, button8_action
from GUI.vb_box_integration import VirtualBoxPreview
from config.system_info import get_system_info
from config.vm_configs import vm_configs_dict
from config.ssh_configs import ssh_config_dict
from config.update_vm_config import update_current_values, update_vm_config
from tkinter import PhotoImage
from GUI import gray_input


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

    title_label = tk.Label(main_tab, text="CyberForge", font=('Arial', 20, 'bold'), fg="#8881fe", bg="#000000")
    title_label.pack(pady=(25, 40))

    def _create_vm_with_disabled_button():
        button1.config(state=tk.DISABLED)
        button1_action()
        button1.config(state=tk.NORMAL)

    actions_group_style = ttk.Style()
    actions_group_style.configure('DarkGrey.TLabelframe', background='#001F3F', font=('Arial', 16, 'bold'))

    actions_group = ttk.LabelFrame(main_tab, style='DarkGrey.TLabelframe')
    actions_group.pack(pady=10)

    button_style = ttk.Style()
    button_style.configure('DarkGrey.TButton', foreground='dark blue')

    button1 = ttk.Button(actions_group, text="New VM", command=_create_vm_with_disabled_button)
    button8 = ttk.Button(actions_group, text="Continue VM", command=button8_action)
    button2 = ttk.Button(actions_group, text="Save VDI", command=button2_action)
    button3 = ttk.Button(actions_group, text="Load VDI", command=button3_action)
    button6 = ttk.Button(actions_group, text="Settings", command=lambda: button6_action(notebook))
    button4 = ttk.Button(actions_group, text="Generate SSH Key", command=button4_action)
    button5 = ttk.Button(actions_group, text="Transfer item", command=button5_action)

    for button in [button1, button8, button2, button3, button4, button5, button6]:
        button.config(width=25, style='DarkGrey.TButton')
        button.pack(side='top', pady=(0, 10), padx=20)

    actions_group.place(relx=0.5, rely=0.5, anchor='center')

    bottom_label = tk.Label(main_tab, text='Build 2.072, Early Access', font=('Arial', 10, 'italic'), fg='#8881fe', bg="#000000")
    bottom_label.place(relx=0.5, rely=0.9, anchor='center')


def setup_config_tab(notebook):
    config_tab = ttk.Frame(notebook)
    notebook.add(config_tab, text='Configuration')

    background_label = tk.Label(config_tab, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    info_label = tk.Label(config_tab, text="If there are empty boxes, the VM will be created with default values.\nFor custom host and port, they must be manually created first.", font=('Arial', 12, 'bold'), fg="#8881fe", bg="#000000")
    info_label.place(relx=0.5, rely=0.9, anchor='center')

    config_group = ttk.LabelFrame(config_tab, text='VM Parameters', style='LightGrey.TLabelframe')
    config_group.place(relx=0.1, rely=0.5, anchor='w')

    labels_and_entries = [
        ("Name:", tk.Entry(config_group)),
        ("RAM Size (in mb):", tk.Entry(config_group)),
        ("Disk Size (in mb):", tk.Entry(config_group)),
        ("CPU Count:", tk.Entry(config_group)),
        ("Host (SSH):", tk.Entry(config_group)),
        ("Port (SSH):", tk.Entry(config_group))
    ]

    for i, (label_text, entry) in enumerate(labels_and_entries):
        label = tk.Label(config_group, text=label_text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
        if entry:
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')

    current_values_frame = ttk.LabelFrame(config_tab, text='Current Creation Info')
    current_values_frame.place(relx=0.6, rely=0.5, anchor='e')
    update_current_values(current_values_frame, vm_configs_dict, ssh_config_dict)

    @wraps
    update_button = tk.Button(config_group, text="Update Config",
                              command=lambda: update_vm_config(
                                  labels_and_entries[0][1], labels_and_entries[1][1],
                                  labels_and_entries[3][1], labels_and_entries[2][1],
                                  labels_and_entries[4][1], labels_and_entries[5][1],
                                  vm_configs_dict, ssh_config_dict, current_values_frame)
                              )
    update_button.grid(row=len(labels_and_entries), column=0, columnspan=2, padx=5, pady=5)



    back_button = tk.Button(config_tab, text="Back", command=lambda: button7_action(notebook))
    back_button.place(relx=0.8, rely=0.8, anchor='se')

    total_ram_gb, cpu_count, disk_details = get_system_info()
    system_info_group = ttk.LabelFrame(config_tab, text='Windows System Info')
    system_info_group.place(relx=0.9, rely=0.1, anchor='ne')

    system_info_labels = [
        f"Total RAM: {total_ram_gb:.2f} GB",
        f"CPU Count: {cpu_count}"
    ] + [f"Free space on {mount_point}: {free_space_gb:.2f} GB" for mount_point, free_space_gb in disk_details.items()]

    for info_text in system_info_labels:
        label = tk.Label(system_info_group, text=info_text)
        label.pack(anchor='w')


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
