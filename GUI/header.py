import tkinter as tk
from tkinter import ttk


class Header(ttk.LabelFrame):
    def __init__(self, master, sign_out_func=None, user_type="guest"):
        super().__init__(master, text="User Status")
        self.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.user_type = tk.StringVar(value=user_type)
        self.user_status_label = ttk.Label(self, text="")
        self.user_status_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.sign_out_button = ttk.Button(self, text="Sign Out", command=sign_out_func)
        self.sign_out_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.update_status()

    def update_status(self):
        user_type = self.user_type.get()
        status_text = f"Logged as {user_type.capitalize()} {'🔒' if user_type == 'admin' else '🔓'}"
        self.user_status_label.config(text=status_text)

    def set_user_type(self, user_type):
        self.user_type.set(user_type)
        self.update_status()

    def set_sign_out_func(self, sign_out_func):
        self.sign_out_button.config(command=sign_out_func)
