import tkinter as tk
from tkinter import simpledialog


def provide_input(title, prompt):
    try:
        root = tk.Tk()
        root.withdraw()

        user_input = simpledialog.askstring(title, prompt, show='~')

        root.destroy()

        if not user_input:
            print("No input detected. Exiting.")
            return None

        return user_input
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
