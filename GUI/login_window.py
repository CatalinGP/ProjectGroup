import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class LoginWindow(tk.Toplevel):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.title("Login")
        self.geometry("300x150")
        self.center_window()

        self.label_username = ttk.Label(self, text="Select User:")
        self.label_username.pack(pady=5)

        self.combo_username = ttk.Combobox(self, values=["admin", "guest"])
        self.combo_username.pack(pady=5)

        self.label_password = ttk.Label(self, text="Password:")
        self.label_password.pack(pady=5)
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = ttk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=5)

        self.on_login = on_login

        # Bind the closing event of this window to the destroy method of the root window
        self.protocol("WM_DELETE_WINDOW", master.destroy)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 300
        window_height = 150
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def login(self):
        username = self.combo_username.get()
        password = self.entry_password.get()

        if (username == "admin" and password == "") or (username == "guest" and password == "guest"):
            self.on_login(username)
            self.destroy()
        else:
            self.show_login_error()

    def show_login_error(self):
        messagebox.showerror("Login Failed", "Invalid username or password")


# Example usage:
def on_login(username):
    print(f"Logged in as {username}")


if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root, on_login)
    root.mainloop()