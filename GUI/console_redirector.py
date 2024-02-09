import tkinter as tk


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.config(state="disabled", bg="#f0f0f0")

    def write(self, text):
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")

    def flush(self):
        pass