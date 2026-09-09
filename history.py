import os
from config import HISTORY_FILE

from encryption import encrypt_data, decrypt_data


def save_history_file(password_history):

    encrypted_data = encrypt_data(password_history)

    with open(HISTORY_FILE, "wb") as file:
        file.write(encrypted_data)


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(HISTORY_FILE, "rb") as file:
            encrypted_data = file.read()

        return decrypt_data(encrypted_data)

    except:

        return []