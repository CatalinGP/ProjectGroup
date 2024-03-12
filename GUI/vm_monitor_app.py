import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from GUI.header import Header
from GUI.login_window import LoginWindow
from GUI.console_redirector import ConsoleRedirector
from GUI.tabs_setup import setup_main_tab, setup_config_tab, setup_log_tab, setup_vm_tab


class VMCPUMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.log_text = None
        self.user_type = None
        self.login_window = None
        self.header = None
        self.notebook = None
        self.init_ui()

    def init_ui(self):
        self.title("Virtual machine monitoring manager")
        self.setup_authentication()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_authentication(self):
        self.withdraw()
        self.login_window = LoginWindow(self, self.on_login)

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
        self.setup_main_frame()

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

        setup_main_tab(notebook)
        setup_config_tab(notebook)
        setup_log_tab(notebook)
        setup_vm_tab(notebook)

        self.notebook = notebook
        self.setup_console_output()
        self.start_monitoring_thread()

    def setup_console_output(self):
        if len(self.notebook.tabs()) >= 3:
            tab3 = self.notebook.tabs()[2]
            tab3_frame = self.notebook.nametowidget(tab3)
            self.log_text = tk.Text(tab3_frame, wrap="word", height=20, width=80)
            self.log_text.grid(row=0, column=0, padx=10, pady=10)
            sys.stdout = ConsoleRedirector(self.log_text)
        else:
            print("Not enough tabs in the notebook.")

    def start_monitoring_thread(self):
        threading.Thread(target=self.monitor_vm, daemon=True).start()

    @staticmethod
    def monitor_vm():
        time.sleep(5)
        print("Monitoring thread started...")
        return True

    def log_update(self, text):
        self.log_text.insert(tk.END, text + '\n')
        self.log_text.see(tk.END)
