from database import db

doc_ref = db.collection("test").document("connection")

doc_ref.set({
    "status": "Connected Successfully"
})

print("✅ Firebase Connected!")