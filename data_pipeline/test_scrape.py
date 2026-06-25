import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
r = requests.get('https://www.myscheme.gov.in/schemes/sui', headers=headers)
print(len(r.text))
if "Stand-Up India" in r.text:
    print("Found scheme details in HTML!")
