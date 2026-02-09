import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# Robust pathing for the environment file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
env_path = os.path.join(project_root, 'api.env')
load_dotenv(env_path)

# OpenAI client is initialized inside the extraction function to support keyless demo mode
def extract_structured_data(text):
    """
    Uses OpenAI API to extract structured data from document text.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Try streamlit secrets as fallback
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENAI_API_KEY")
        except:
            pass

    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment or secrets.")
        return None
        
    client = OpenAI(api_key=api_key)
    if not text:
        return None

    prompt = f"""
    You are an expert document processing AI. Extract information from the following invoice/receipt text into a structured JSON format.
    
    TEXT:
    {text}
    
    EXTRACT THE FOLLOWING FIELDS:
    - document_type (Invoice, Receipt, or Other)
    - invoice_number
    - date (YYYY-MM-DD format if possible)
    - vendor_name
    - total_amount (numeric only)
    - currency (e.g., USD, EUR, GBP)
    - tax_amount (numeric only)
    - payment_terms
    - line_items (list of objects with: description, quantity, unit_price, subtotal)
    
    ALSO PROVIDE:
    - field_confidence (a dictionary with confidence scores 0-100 for each field above)
    - overall_confidence (0-100)
    
    RETURN ONLY VALID JSON.
    """

    try:
    # List of models to try in order of preference
    models_to_try = [
        "gpt-4.1-nano-2025-04-14", # Most cost-effective
        "gpt-4o-mini"              # Robust fallback
    ]
    
    last_exception = None
    
    for model_name in models_to_try:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured data from text and returns it in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            extracted_json = json.loads(response.choices[0].message.content)
            return extracted_json
        except Exception as e:
            last_exception = e
            print(f"Model {model_name} failed: {e}")
            continue

    print(f"All models failed. Last error: {last_exception}")
    return None

if __name__ == "__main__":
    # Test with mockup text
    test_text = "Invoice #INV-123\nDate: 2023-10-25\nVendor: ACME Corp\nTotal: $150.00\nTax: $10.00\nItems: \n1x widget @ $140.00"
    print("Testing AI extraction...")
    result = extract_structured_data(test_text)
    print(json.dumps(result, indent=2) if result else "Extraction failed.")
