import bcrypt
import os

MASTER_PASSWORD_FILE = "data/master.hash"


def master_password_exists():
    return os.path.exists(MASTER_PASSWORD_FILE)


def set_master_password(password):

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    with open(MASTER_PASSWORD_FILE, "wb") as file:
        file.write(hashed)


def verify_master_password(password):

    if not master_password_exists():
        return False

    with open(MASTER_PASSWORD_FILE, "rb") as file:
        hashed = file.read()

    return bcrypt.checkpw(
        password.encode(),
        hashed
    )