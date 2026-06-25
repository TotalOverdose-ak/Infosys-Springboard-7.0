"""
Fetch ALL 4730 schemes from MyScheme.gov.in API and upload to Firebase
"""
import requests, json, uuid, time, ssl, urllib3
urllib3.disable_warnings()
import requests.adapters

class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount("https://", TLSAdapter())
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"c:\Users\AkashK\Desktop\Infosys Springboard 7.0\Subsidy_Project\backend\src\main\resources\serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

API_KEY = "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc"
HEADERS = {
    "x-api-key": API_KEY,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Origin": "https://www.myscheme.gov.in",
    "Referer": "https://www.myscheme.gov.in/",
}

def fetch_all():
    schemes = []
    offset = 0
    size = 50
    total = 99999
    
    while offset < total:
        url = f"https://api.myscheme.gov.in/search/v6/schemes?lang=en&q=%5B%5D&keyword=&sort=&from={offset}&size={size}"
        r = session.get(url, headers=HEADERS, timeout=15, verify=False)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code} at offset {offset}")
            break
        
        data = r.json()
        hits = data.get("data", {}).get("hits", {})
        items = hits.get("items", [])
        page_info = hits.get("page", {})
        total = page_info.get("total", 0)
        
        if not items:
            break
        
        for item in items:
            f = item.get("fields", {})
            title = f.get("schemeName", "")
            slug = f.get("slug", "")
            cats = f.get("schemeCategory", ["Social Welfare"])
            states = f.get("beneficiaryState", ["All States"])
            state = states[0] if states else "All States"
            cat = cats[0] if cats else "Social Welfare"
            
            if title:
                schemes.append({
                    "title": title,
                    "description": f.get("briefDescription", "") or "Visit myscheme.gov.in for detailed information about this scheme",
                    "eligibilityCriteria": "Visit myscheme.gov.in for eligibility",
                    "state": state,
                    "category": cat,
                    "amount": 0,
                    "applicationDeadline": f.get("schemeCloseDate", "2026-12-31") or "2026-12-31",
                    "applicationUrl": f"https://www.myscheme.gov.in/schemes/{slug}",
                    "active": True
                })
        
        offset += size
        print(f"  Fetched {offset}/{total} schemes...")
        time.sleep(0.2)
    
    return schemes

def upload(schemes):
    existing = set()
    for doc in db.collection("subsidies").stream():
        existing.add(doc.to_dict().get("title", "").lower().strip())
    added = 0
    batch = db.batch()
    for s in schemes:
        key = s["title"].lower().strip()
        if key in existing or not s["title"]:
            continue
        s["id"] = str(uuid.uuid4())
        ref = db.collection("subsidies").document(s["id"])
        batch.set(ref, s)
        existing.add(key)
        added += 1
        if added % 450 == 0:
            batch.commit()
            batch = db.batch()
            print(f"  Committed {added}...")
    batch.commit()
    return added

if __name__ == "__main__":
    print("=" * 50)
    print("MYSCHEME FETCHER - ALL 4730 SCHEMES")
    print("=" * 50)
    schemes = fetch_all()
    print(f"\nFetched: {len(schemes)}")
    print("Uploading to Firestore...")
    added = upload(schemes)
    total = len(list(db.collection("subsidies").stream()))
    print(f"\nDONE! Added: {added} | Total in DB: {total}")
