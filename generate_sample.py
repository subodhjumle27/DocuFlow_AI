from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_invoice(filename):
    if not os.path.exists("samples"):
        os.makedirs("samples")
    
    path = os.path.join("samples", filename)
    c = canvas.Canvas(path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "INVOICE")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "ACME Solutions Inc.")
    c.drawString(50, height - 95, "123 Business Way, Tech City")
    c.drawString(50, height - 110, "Email: billing@acme.com")
    
    # Invoice Details
    c.drawString(400, height - 80, "Invoice #: INV-2026-001")
    c.drawString(400, height - 95, "Date: 2026-02-09")
    c.drawString(400, height - 110, "Payment Terms: Net 30")
    
    # Bill To
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 160, "BILL TO:")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 175, "Global Enterprises Ltd.")
    c.drawString(50, height - 190, "456 Enterprise Dr.")
    c.drawString(50, height - 205, "Finance Dept.")
    
    # Table Header
    c.line(50, height - 230, 550, height - 230)
    c.drawString(50, height - 245, "Description")
    c.drawString(300, height - 245, "Quantity")
    c.drawString(400, height - 245, "Unit Price")
    c.drawString(500, height - 245, "Total")
    c.line(50, height - 250, 550, height - 250)
    
    # Items
    c.drawString(50, height - 270, "Cloud Hosting Service - Annual")
    c.drawString(300, height - 270, "1")
    c.drawString(400, height - 270, "$1,200.00")
    c.drawString(500, height - 270, "$1,200.00")
    
    c.drawString(50, height - 290, "Technical Support Subscription")
    c.drawString(300, height - 290, "12")
    c.drawString(400, height - 290, "$50.00")
    c.drawString(500, height - 290, "$600.00")
    
    # Totals
    c.line(400, height - 330, 550, height - 330)
    c.drawString(400, height - 345, "Subtotal:")
    c.drawString(500, height - 345, "$1,800.00")
    
    c.drawString(400, height - 360, "Tax (10%):")
    c.drawString(500, height - 360, "$180.00")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, height - 380, "TOTAL DUE:")
    c.drawString(500, height - 380, "$1,980.00")
    c.setFont("Helvetica", 12)
    
    c.drawString(50, height - 450, "Notes: Please make payment by bank transfer.")
    c.drawString(50, height - 465, "Thank you for your business!")
    
    c.save()
    print(f"Sample invoice created at: {path}")

if __name__ == "__main__":
    create_sample_invoice("sample_invoice.pdf")
