"""
Intercept XHR calls from MyScheme.gov.in to find the real API endpoint
"""
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import json, time

opts = Options()
opts.add_argument("--disable-gpu")
opts.add_argument("--window-size=1920,1080")
opts.set_capability("ms:loggingPrefs", {"performance": "ALL"})

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=opts)

try:
    driver.get("https://www.myscheme.gov.in/search")
    time.sleep(10)
    
    # Get performance logs to find API calls
    logs = driver.get_log("performance")
    api_calls = []
    for entry in logs:
        msg = json.loads(entry["message"])["message"]
        if msg["method"] == "Network.requestWillBeSent":
            url = msg["params"]["request"]["url"]
            method = msg["params"]["request"]["method"]
            if "api" in url.lower() or "scheme" in url.lower():
                headers = msg["params"]["request"].get("headers", {})
                body = msg["params"]["request"].get("postData", "")
                print(f"\n{method} {url}")
                if body:
                    print(f"  Body: {body[:200]}")
                # Print key headers
                for k, v in headers.items():
                    if k.lower() in ('authorization', 'x-api-key', 'content-type', 'cookie'):
                        print(f"  {k}: {v[:100]}")
finally:
    driver.quit()
