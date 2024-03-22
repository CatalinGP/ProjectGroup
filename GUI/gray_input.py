import login_window


def verify_user_guest_or_admin(fn):
    @wraps(fn)
    def wrapper():
        result = login_window.create_login_window(dropdown_users=True)
        if result:
            username, _ = result
            if username == "admin":
                return fn
            elif username == "guest":
                disable_input()
            else:
                return "Invalid account"
    return wrapper


def disable_input(input_entries):
    for entry in input_entries:
        entry.config(state="disabled")

