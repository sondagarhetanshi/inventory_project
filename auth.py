from database import add_user, login_user

def register(username, password):
    add_user(username, password)
    return "User Created"

def login(username, password):
    user = login_user(username, password)

    if user:
        return True
    return False