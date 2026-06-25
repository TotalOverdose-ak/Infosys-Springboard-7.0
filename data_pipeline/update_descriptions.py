import requests, json, time, ssl, urllib3
urllib3.disable_warnings()
import requests.adapters
import firebase_admin
from firebase_admin import credentials, firestore

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

cred = credentials.Certificate(r"c:\Users\AkashK\Desktop\Infosys Springboard 7.0\Subsidy_Project\backend\src\main\resources\serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7",
    "Origin": "https://www.myscheme.gov.in",
    "Referer": "https://www.myscheme.gov.in/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-api-key": "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc",
    "x-client": "myscheme-ui"
}

def fetch_and_update():
    existing_docs = {}
    for doc in db.collection("subsidies").stream():
        d = doc.to_dict()
        if "title" in d:
            existing_docs[d["title"].lower().strip()] = doc.reference

    print(f"Found {len(existing_docs)} existing schemes in DB.")

    offset = 0
    size = 50
    total = 50
    updated = 0
    batch = db.batch()

    while offset < total:
        url = f"https://api.myscheme.gov.in/search/v6/schemes?lang=en&q=%5B%5D&keyword=&sort=&from={offset}&size={size}"
        r = session.get(url, headers=HEADERS, timeout=15, verify=False)
        if r.status_code != 200:
            print(f"Failed at offset {offset}")
            break
        
        res = r.json()
        if 'data' not in res or 'hits' not in res['data']:
            print("Invalid structure")
            break
            
        data = res['data']
        hits = data.get("hits", {})
        items = hits.get("items", [])
        total = hits.get("page", {}).get("total", 0)
        print(f"Fetched {len(items)} items from offset {offset}. Total: {total}")

        for item in items:
            f = item.get("fields", {})
            title = f.get("schemeName", "").lower().strip()
            new_desc = f.get("briefDescription", "")

            if title in existing_docs and new_desc:
                batch.update(existing_docs[title], {"description": new_desc})
                updated += 1

                if updated % 450 == 0:
                    batch.commit()
                    batch = db.batch()
                    print(f"Committed {updated} updates...")

        offset += size
        time.sleep(0.1)

    batch.commit()
    print(f"Successfully updated {updated} descriptions!")

if __name__ == "__main__":
    fetch_and_update()
