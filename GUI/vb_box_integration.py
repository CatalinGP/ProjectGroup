import subprocess
import win32gui
import tkinter as tk
from tkinter import ttk

class VirtualBoxPreview:
    def __init__(self, parent):
        self.parent = parent
        self.preview_window = tk.Toplevel()  # Create a Toplevel window for the preview
        self.preview_window.geometry("200x200")  # Set window geometry for the preview window
        self.virtualbox_process = subprocess.Popen(["C:\\Program Files\\Oracle\\VirtualBox\\VirtualBox.exe"])
        self.embed_vm_window()

    def embed_vm_window(self):
        self.preview_window.after(100, self.embed_vm_window_after_delay)

    def embed_vm_window_after_delay(self):
        self.virtualbox_handle = None
        while not self.virtualbox_handle:
            self.virtualbox_handle = win32gui.FindWindow(None, "Oracle VM VirtualBox Manager")

        self.vm_handle = None
        while not self.vm_handle:
            self.vm_handle = win32gui.FindWindowEx(self.virtualbox_handle, 0, "OracleVirtualBoxMachineWindowClass", None)

        frame_handle = self.preview_window.winfo_id()
        win32gui.SetParent(self.vm_handle, frame_handle)
        win32gui.MoveWindow(self.vm_handle, 0, 0, self.preview_window.winfo_width(),
                            self.preview_window.winfo_height(), True)

