import subprocess
import sys
import threading
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from GUI.header import Header
from GUI.login_window import create_login_window
from GUI.console_redirector import ConsoleRedirector
from GUI.tabs_setup import (setup_main_tab,
                            setup_config_tab,
                            setup_log_tab,
                            setup_vm_tab)
from scripts.ssh.ssh_utils import SSHKeyManager


def monitor_vm(stop_event):
    while not stop_event.is_set():
        ssh_manager = SSHKeyManager()
        login_result = create_login_window(dropdown_users=False, require_password=False)
        user, password = login_result

        ip_address = ssh_manager.get_remote_ip(user)

        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip_address]

        try:
            response = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if response.returncode == 0:
                return 200
            else:
                return 503
        except subprocess.SubprocessError:
            return 503


class VMCPUMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.stop_event = None
        self.header = None
        self.username = None
        self.notebook = None
        self.user_type = None
        self.login_window = None
        self.init_ui()
        self.monitoring_thread = None

    def init_ui(self):
        self.title("Virtual machine monitoring manager")
        self.setup_authentication()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_logout(self):
        """
        Handle user logout, reset the state, and show the login window.
        """
        self.username = None
        self.user_type = None
        if self.monitoring_thread:
            self.stop_event.set()
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_authentication()

    def setup_authentication(self):
        self.withdraw()
        login_result = create_login_window(parent=self, dropdown_users=True, require_password=False)
        if login_result:
            username, user_type = login_result
            self.username = username
            self.user_type = user_type
            self.deiconify()
            self.setup_window()
        else:
            self.destroy()

    def setup_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_geometry()
        self.notebook = self.setup_main_frame()
        self.setup_tabs()
        self.setup_console_output()
        self.start_threads()

    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.destroy()

    def setup_geometry(self):
        self.geometry("800x600")

    def setup_main_frame(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.header = Header(main_frame, user_type=self.user_type, username=self.username, sign_out_func=self.on_logout)
        self.header.grid(row=0, column=0, sticky="nsew")

        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky="nsew")
        return notebook

    def setup_tabs(self):
        setup_main_tab(self.notebook)
        setup_config_tab(self.notebook)
        setup_log_tab(self.notebook)
        setup_vm_tab(self.notebook)

    def setup_console_output(self):
        if len(self.notebook.tabs()) >= 3:
            tab3 = self.notebook.tabs()[2]
            tab3_frame = self.notebook.nametowidget(tab3)
            log_text = tk.Text(tab3_frame, wrap="word", height=20, width=80)
            log_text.grid(row=0, column=0, padx=10, pady=10)
            sys.stdout = ConsoleRedirector(log_text)
        else:
            print("Not enough tabs in the notebook.")

    def start_threads(self):
        self.stop_event = threading.Event()
        self.monitoring_thread = threading.Thread(target=monitor_vm, args=(self.stop_event,), daemon=True)
        self.monitoring_thread.start()
        return self.stop_event
