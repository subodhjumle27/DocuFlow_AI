from datetime import datetime

def validate_extraction(data):
    """
    Validates the extracted data against business rules.
    Returns a dictionary of results (pass/fail per rule).
    """
    results = {
        "is_valid": True,
        "rules": []
    }
    
    # 1. Required fields check
    required_fields = ["vendor_name", "date", "total_amount"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        results["is_valid"] = False
        results["rules"].append({"rule": "Required Fields", "status": "FAIL", "message": f"Missing: {', '.join(missing_fields)}"})
    else:
        results["rules"].append({"rule": "Required Fields", "status": "PASS", "message": "All required fields present."})
        
    # 2. Date validation
    date_str = data.get("date")
    if date_str:
        try:
            doc_date = datetime.strptime(date_str, "%Y-%m-%d")
            if doc_date > datetime.now():
                results["is_valid"] = False
                results["rules"].append({"rule": "Date Validity", "status": "FAIL", "message": "Date is in the future."})
            else:
                results["rules"].append({"rule": "Date Validity", "status": "PASS", "message": "Date is valid."})
        except:
             results["rules"].append({"rule": "Date Validity", "status": "WARNING", "message": "Could not parse date format."})

    # 3. Total amount validation
    amount = data.get("total_amount")
    if amount is not None:
        try:
            val = float(amount)
            if val < 0:
                results["is_valid"] = False
                results["rules"].append({"rule": "Amount Check", "status": "FAIL", "message": "Amount is negative."})
            elif val > 10000:
                results["rules"].append({"rule": "Amount Check", "status": "WARNING", "message": "High value document (>$10,000)."})
            else:
                results["rules"].append({"rule": "Amount Check", "status": "PASS", "message": "Amount is within normal range."})
        except:
            results["is_valid"] = False
            results["rules"].append({"rule": "Amount Check", "status": "FAIL", "message": "Amount is not a valid number."})

    return results
