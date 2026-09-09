import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from encryption import encrypt_for_cloud, decrypt_from_cloud

cred = credentials.Certificate("data/firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
def upload_history(email, history):

    encrypted_history = encrypt_for_cloud(history)
    db.collection("users").document(email).set({

        "history": encrypted_history,

        "last_sync": datetime.now().isoformat()

    })
    
    return True
def download_history(email):

    doc = db.collection("users").document(email).get()

    if doc.exists:

        data = doc.to_dict()

        encrypted_history = data.get("history")
        if isinstance(encrypted_history, list):
            return encrypted_history

        return decrypt_from_cloud(encrypted_history)

    return []
def delete_cloud_history(email):

    db.collection("users").document(email).delete()