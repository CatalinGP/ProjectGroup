import tkinter as tk
from tkinter import ttk


def create_login_window(username_label="Username:",
                        password_label="Password:",
                        login_button="Login",
                        require_password=True,
                        dropdown_users=False,
                        parent=None):

    def login():
        if dropdown_users:
            username = username_var.get()
        else:
            username = username_entry.get()
        password = password_var.get() if require_password else None
        if not username:
            show_error("Username cannot be empty!")
            return
        if require_password and not password:
            show_error("Password cannot be empty!")
            return
        window.destroy()
        window.result = (username, password)

    def show_error(message):
        error_label.config(text=message)
        error_label.pack()

    window = tk.Toplevel(parent)
    window.title("Login Window")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 300
    window_height = 200 if require_password else 170

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    password_var = tk.StringVar()

    if dropdown_users:
        username_var = tk.StringVar(value="admin")
        username_label = ttk.Label(window, text=username_label)
        username_label.pack(pady=5)
        username_dropdown = ttk.Combobox(window, textvariable=username_var, values=["admin", "guest"])
        username_dropdown.pack(pady=5)
    else:
        username_var = tk.StringVar()
        username_label_widget = ttk.Label(window, text=username_label)
        username_label_widget.pack(pady=5)
        username_entry = ttk.Entry(window, textvariable=username_var)
        username_entry.pack(pady=5)

    if require_password:
        password_label_widget = ttk.Label(window, text=password_label)
        password_label_widget.pack(pady=5)
        password_entry = ttk.Entry(window, show="*", textvariable=password_var)
        password_entry.pack(pady=5)

    login_button_widget = ttk.Button(window, text=login_button, command=login)
    login_button_widget.pack(pady=10)

    error_label = ttk.Label(window, foreground="red")

    window.grab_set()
    window.wait_window(window)
    return window.result if hasattr(window, 'result') else None
