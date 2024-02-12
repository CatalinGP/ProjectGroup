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
            # Find the handle of the VirtualBox Manager window
            vbox_manager_handle = win32gui.FindWindow(None, "Oracle VM VirtualBox Manager")

            if vbox_manager_handle:
                # Find the handle of the virtual machine window
                vm_handle = win32gui.FindWindowEx(vbox_manager_handle, 0, "OracleVirtualBoxMachineWindowClass", self.vm_title)

                if vm_handle:
                    # Get the position and size of the virtual machine window
                    left, top, right, bottom = win32gui.GetWindowRect(vm_handle)

                    # Capture a screenshot of the virtual machine window
                    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

                    # Resize the screenshot to fit the preview label
                    screenshot = screenshot.resize((300, 200), ImageGrab.Image.ANTIALIAS)

                    # Convert the screenshot to a Tkinter compatible format
                    photo = ImageTk.PhotoImage(screenshot)

                    # Update the preview label with the new screenshot
                    self.preview_label.configure(image=photo)
                    self.preview_label.image = photo
                else:
                    # Virtual machine window not found
                    self.preview_label.configure(text="Virtual machine window not found")
            else:
                # VirtualBox Manager window not found
                self.preview_label.configure(text="VirtualBox Manager not found")

        except Exception as e:
            print("Error updating preview:", e)

        # Schedule the next update
        self.parent_frame.after(self.update_interval, self.update_preview)
