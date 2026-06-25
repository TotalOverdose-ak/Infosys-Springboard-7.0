import json
import random
from datetime import datetime, timedelta

# Categories mapped to typical documents
category_documents = {
    "Agriculture": ["Aadhar Card", "Land Ownership Proof (7/12 Extract)", "Bank Account Details", "Passport Size Photograph", "Farmer Certificate"],
    "Education": ["Aadhar Card", "Previous Year Marksheet", "Income Certificate", "Bonafide Certificate from College", "Bank Account Details", "Caste Certificate (if applicable)"],
    "Women Empowerment": ["Aadhar Card", "Income Certificate", "Ration Card", "Bank Passbook Copy", "Domicile Certificate"],
    "Health": ["Aadhar Card", "Medical Certificate / Report", "Income Certificate", "Hospital Admission Proof", "BPL Ration Card"],
    "Business": ["Aadhar Card", "PAN Card", "Project Report", "Bank Account Statement", "Business Registration Proof", "Quotation for Machinery/Equipment"],
    "General": ["Aadhar Card", "Income Certificate", "Bank Account Details", "Passport Size Photograph", "Domicile Certificate"]
}

file_path = r"c:\Users\AkashK\Desktop\Infosys Springboard 7.0\Subsidy_Project\backend\src\main\resources\data\schemes.json"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        schemes = json.load(f)
        
    for scheme in schemes:
        category = scheme.get("category", "General")
        pool = category_documents.get(category, category_documents["General"])
        
        # Pick 3-5 random documents based on category
        num_docs = random.randint(3, len(pool))
        docs = random.sample(pool, num_docs)
        if "Aadhar Card" not in docs:
            docs.insert(0, "Aadhar Card")
            
        scheme["documentsRequired"] = docs
        
        # Assign a random deadline between today + 15 days to today + 365 days
        days_ahead = random.randint(15, 365)
        deadline = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        scheme["applicationDeadline"] = deadline

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(schemes, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully mutated {len(schemes)} schemes with dynamic documents and deadlines!")

except Exception as e:
    print("Error:", e)
