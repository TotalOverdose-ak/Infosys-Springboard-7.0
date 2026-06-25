import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"c:\Users\AkashK\Desktop\Infosys Springboard 7.0\Subsidy_Project\backend\src\main\resources\serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

try:
    docs = db.collection("subsidies").limit(1).stream()
    for doc in docs:
        print("Success! Can read:", doc.id)
except Exception as e:
    print("Failed:", e)
