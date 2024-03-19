import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from GUI.header import Header
from GUI.login_window import LoginWindow
from GUI.login_win import create_login_window
from GUI.console_redirector import ConsoleRedirector
from GUI.tabs_setup import setup_main_tab, setup_config_tab, setup_log_tab, setup_vm_tab


def monitor_vm():
    time.sleep(5)
    print("Monitoring thread started...")
    return True


class VMCPUMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.notebook = None
        self.user_type = None
        self.login_window = None
        self.init_ui()

    def init_ui(self):
        self.title("Virtual machine monitoring manager")
        self.setup_authentication()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_authentication(self):
        self.withdraw()
        self.login_window = LoginWindow(self, self.on_login)
        login_result = create_login_window(dropdown_users=False, require_password=False)
        user, password = login_result


    def on_login(self, user_type):
        self.deiconify()
        self.user_type = user_type
        self.setup_window()

    def sign_out(self):
        self.withdraw()
        self.login_window = LoginWindow(self, self.on_login)
        self.user_type = None

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

        header = Header(main_frame, sign_out_func=self.sign_out, user_type=self.user_type)
        header.grid(row=0, column=0, sticky="nsew")

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

    @staticmethod
    def start_threads():
        threading.Thread(target=monitor_vm, daemon=True).start()
