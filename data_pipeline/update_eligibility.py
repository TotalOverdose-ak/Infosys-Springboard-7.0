import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"c:\Users\AkashK\Desktop\Infosys Springboard 7.0\Subsidy_Project\backend\src\main\resources\serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def update_eligibility():
    batch = db.batch()
    updated = 0
    new_eligibility = "Eligibility varies based on applicant demographic, income, and state guidelines. Please proceed to the Application Form to submit your details for verification."
    
    for doc in db.collection("subsidies").stream():
        batch.update(doc.reference, {"eligibilityCriteria": new_eligibility})
        updated += 1
        
        if updated % 450 == 0:
            batch.commit()
            batch = db.batch()
            print(f"Committed {updated} updates...")
            
    batch.commit()
    print(f"Successfully updated {updated} eligibility criteria!")

if __name__ == "__main__":
    update_eligibility()
