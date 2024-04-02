from functools import wraps
from GUI import login_window
from config import update_vm_config


def verify_user_and_disable(fn):
    @wraps(fn)
    def wrapper():
        result = login_window.create_login_window(dropdown_users=True)
        if result:
            username, _ = result
            if username == "admin":
                return fn()
            elif username == "guest":
                disable_input(update_vm_config)
            else:
                return "Invalid account"
    return wrapper


def disable_input(input_data):
    if hasattr(input_data, '__iter__'):
        for entry in input_data:
            entry.config(state="disabled")
    else:
        for entry in input_data:
            entry.config(state="disabled")
