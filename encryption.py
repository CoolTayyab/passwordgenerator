import os
import json
import base64
import hashlib
from cryptography.fernet import Fernet
from config import KEY_FILE
def get_key():

    if not os.path.exists(KEY_FILE):

        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

    else:

        with open(KEY_FILE, "rb") as file:
            key = file.read()

    return key
key = get_key()
cipher = Fernet(key)
#def get_cipher(master_password):

    #key = hashlib.sha256(
        #master_password.encode()
    #).digest()

    #key = base64.urlsafe_b64encode(key)

    #return Fernet(key)

def encrypt_data(data):

    json_data = json.dumps(data)

    return cipher.encrypt(
        json_data.encode()
    )
def decrypt_data(encrypted_data):

    decrypted = cipher.decrypt(
        encrypted_data
    )

    return json.loads(
        decrypted.decode()
    )
def encrypt_for_cloud(data):

    json_data = json.dumps(data)

    encrypted = cipher.encrypt(
        json_data.encode()
    )

    return encrypted.decode()


def decrypt_from_cloud(data):

    decrypted = cipher.decrypt(
        data.encode()
    )

    return json.loads(
        decrypted.decode()
    )
    