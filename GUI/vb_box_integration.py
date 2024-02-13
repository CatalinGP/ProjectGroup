import tkinter as tk
from PIL import ImageGrab, ImageTk
import win32gui

class VirtualBoxPreview:
    def __init__(self, parent_frame, vm_title, update_interval=1000):
        self.parent_frame = parent_frame
        self.vm_title = vm_title
        self.update_interval = update_interval
        self.preview_label = tk.Label(parent_frame)
        self.preview_label.pack()
        self.update_preview()

    def update_preview(self):
        try:
            vbox_manager_handle = win32gui.FindWindow(None, "Oracle VM VirtualBox Manager")

            if vbox_manager_handle:
                vm_handle = win32gui.FindWindowEx(vbox_manager_handle,
                                                  0,
                                                  "OracleVirtualBoxMachineWindowClass",
                                                  self.vm_title)

                if vm_handle:
                    left, top, right, bottom = win32gui.GetWindowRect(vm_handle)
                    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
                    screenshot = screenshot.resize((300, 200), ImageGrab.Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(screenshot)
                    self.preview_label.configure(image=photo)
                    self.preview_label.image = photo
                else:
                    self.preview_label.configure(text="Virtual machine window not found")
            else:
                self.preview_label.configure(text="VirtualBox Manager not found")

        except Exception as e:
            print("Error updating preview:", e)

        self.parent_frame.after(self.update_interval, self.update_preview)
