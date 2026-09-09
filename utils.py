import pyperclip
import socket

def copy_to_clipboard(app, text):

    app.clipboard_clear()
    app.clipboard_append(text)

import random
import string

def generate_random_password(
    length,
    uppercase,
    lowercase,
    numbers,
    symbols
):

    chars = ""

    if uppercase:
        chars += string.ascii_uppercase

    if lowercase:
        chars += string.ascii_lowercase

    if numbers:
        chars += string.digits

    if symbols:
        chars += "!@#$%^&*()_-+=<>?/"

    if not chars:
        return ""

    return "".join(
        random.choice(chars)
        for _ in range(length)
    )
def is_connected():

    try:

        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        return True

    except OSError:

        return False
