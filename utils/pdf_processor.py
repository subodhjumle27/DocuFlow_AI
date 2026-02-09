import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

if __name__ == "__main__":
    # Test extraction if a sample exists
    test_pdf = "samples/invoice1.pdf"
    if os.path.exists(test_pdf):
        print(f"Extracting text from {test_pdf}...")
        text = extract_text_from_pdf(test_pdf)
        print("Extracted Text Preview:")
        print(text[:500] if text else "No text extracted.")
    else:
        print(f"Sample PDF {test_pdf} not found.")
