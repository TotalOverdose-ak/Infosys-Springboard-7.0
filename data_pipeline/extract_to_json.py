import requests, json, time, ssl, urllib3, uuid
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

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7",
    "Origin": "https://www.myscheme.gov.in",
    "Referer": "https://www.myscheme.gov.in/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-api-key": "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc",
    "x-client": "myscheme-ui"
}

def extract_all():
    offset = 0
    size = 50
    total = 50
    all_schemes = []

    # Format the data according to the Java Subsidy model
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
            subsidy_data = {
                "id": str(uuid.uuid4()),
                "title": f.get("schemeName", "Unknown Scheme"),
                "description": f.get("briefDescription", "") or "This government scheme provides financial assistance and welfare benefits to eligible citizens. Please visit the official MyScheme portal for comprehensive guidelines, required documents, and eligibility criteria.",
                "amount": 0.0,
                "eligibilityCriteria": "Eligibility varies based on applicant demographic, income, and state guidelines. Please proceed to the Application Form to submit your details for verification.",
                "applicationDeadline": f.get("schemeCloseDate", "2026-12-31") or "2026-12-31",
                "state": f.get("beneficiaryState", ["All States"])[0] if f.get("beneficiaryState") else "All States",
                "category": f.get("schemeCategory", ["General"])[0] if f.get("schemeCategory") else "General",
                "isActive": True,
                "isExpired": False,
                "ministry": f.get("nodalMinistryName", "Govt of India")
            }
            all_schemes.append(subsidy_data)

        offset += size
        time.sleep(0.1)

    output_path = r"c:\Users\AkashK\Desktop\Infosys Springboard 7.0\Subsidy_Project\backend\src\main\resources\data\schemes.json"
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(all_schemes, file, ensure_ascii=False, indent=4)
    
    print(f"Successfully saved {len(all_schemes)} schemes to {output_path}")

if __name__ == "__main__":
    extract_all()
