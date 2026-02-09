import streamlit as st
import os
import pandas as pd
import time
import json
from utils.validator import validate_extraction
from utils.confidence import calculate_status, get_confidence_color
from utils.pdf_processor import extract_text_from_pdf
from utils.ai_extractor import extract_structured_data

# Page config
st.set_page_config(page_title="DocuFlow AI", layout="wide", page_icon="📑")

# Custom CSS for modern look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .status-approved { background-color: #d4edda; color: #155724; }
    .status-review { background-color: #fff3cd; color: #856404; }
    .card {
        padding: 20px;
        border-radius: 12px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation & settings
st.sidebar.markdown("# 🚀 DocuFlow AI")
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Navigation", ["Upload", "Review Queue", "Dashboard"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Settings")
demo_mode = st.sidebar.toggle("Demo Mode (Mock Extracts)", value=False, help="Use this for stable demoing without API calls.")

# "Database" file
DB_FILE = "documents_data.csv"

def get_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["id", "filename", "status", "confidence", "vendor", "date", "total", "type", "timestamp", "extracted_json"])
    try:
        df = pd.read_csv(DB_FILE)
        return df
    except:
        return pd.DataFrame(columns=["id", "filename", "status", "confidence", "vendor", "date", "total", "type", "timestamp", "extracted_json"])

def save_to_db(doc_data, extracted_data, status):
    df = get_data()
    next_id = len(df) + 1
    new_row = {
        "id": next_id,
        "filename": doc_data["filename"],
        "status": status,
        "confidence": extracted_data["overall_confidence"],
        "vendor": extracted_data.get("vendor_name", "N/A"),
        "date": extracted_data.get("date", "N/A"),
        "total": extracted_data.get("total_amount", 0),
        "type": extracted_data.get("document_type", "N/A"),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "extracted_json": json.dumps(extracted_data)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def update_doc_status(doc_id, new_status, updated_json=None):
    df = get_data()
    if updated_json:
        df.loc[df['id'] == doc_id, 'extracted_json'] = json.dumps(updated_json)
        df.loc[df['id'] == doc_id, 'vendor'] = updated_json.get('vendor_name')
        df.loc[df['id'] == doc_id, 'total'] = updated_json.get('total_amount')
        df.loc[df['id'] == doc_id, 'date'] = updated_json.get('date')
    
    df.loc[df['id'] == doc_id, 'status'] = new_status
    df.to_csv(DB_FILE, index=False)

def mock_extract(filename):
    """Fallback mock extraction for demos."""
    return {
        "document_type": "Invoice",
        "invoice_number": "MOCK-12345",
        "date": "2026-02-09",
        "vendor_name": "Mock Vendor Corp.",
        "total_amount": 1980.00,
        "currency": "USD",
        "overall_confidence": 92,
        "line_items": [{"description": "Cloud Services", "quantity": 1, "unit_price": 1980.0, "subtotal": 1980.0}]
    }

if page == "Upload":
    # Hero Section
    st.markdown("""
        <div style='background-color: #007bff; padding: 40px; border-radius: 15px; color: white; margin-bottom: 30px;'>
            <h1 style='color: white; margin-bottom: 5px;'>Modern AI Invoice Processing</h1>
            <p style='font-size: 1.2em; opacity: 0.9;'>Extract structured data from your financial documents in seconds with human-in-the-loop verification.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        uploaded_file = st.file_uploader("📂 Drag and drop your PDF here", type="pdf")
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info(f"📍 **Selected:** {uploaded_file.name}")
            
            # Save file
            if not os.path.exists("public_samples"):
                os.makedirs("public_samples")
            pdf_path = os.path.join("public_samples", uploaded_file.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if st.button("🚀 Start AI Extraction", type="primary"):
                with st.spinner("Analyzing document structure..."):
                    if demo_mode:
                        time.sleep(1.5)
                        extracted_data = mock_extract(uploaded_file.name)
                    else:
                        text = extract_text_from_pdf(pdf_path)
                        if text:
                            extracted_data = extract_structured_data(text)
                        else:
                            st.error("❌ No text extracted from PDF.")
                            extracted_data = None
                            
                    if extracted_data:
                        v_results = validate_extraction(extracted_data)
                        status = calculate_status(extracted_data['overall_confidence'], v_results)
                        save_to_db({"filename": uploaded_file.name}, extracted_data, status)
                        
                        if status == "approved":
                            st.success("✨ **Auto-Approved!** Content matches all business rules.")
                            st.balloons()
                        else:
                            st.warning("⚠️ **Needs Review.** Confidence threshold low or validation warnings found.")
                        
                        st.markdown("---")
                        st.markdown("### 📊 Extraction Preview")
                        st.json(extracted_data)

elif page == "Review Queue":
    st.title("📋 Manual Review Queue")
    st.write("Documents requiring human oversight due to low confidence or validation flags.")
    
    df = get_data()
    review_docs = df[df['status'] == 'needs_review']
    
    if review_docs.empty:
        st.success("🎉 **Queue Empty!** All documents are processed and approved.")
    else:
        for _, doc in review_docs.iterrows():
            with st.expander(f"Review Item: {doc['filename']} (Confidence: {doc['confidence']}%)", expanded=True):
                col1, col2 = st.columns([1.5, 1])
                current_data = json.loads(doc['extracted_json'])
                
                with col1:
                    st.markdown("#### ✏️ Verify Data")
                    v_name = st.text_input("Company/Vendor", value=current_data.get('vendor_name'), key=f"v_{doc['id']}")
                    v_date = st.text_input("Doc Date", value=current_data.get('date'), key=f"d_{doc['id']}")
                    v_amount = st.number_input("Total Due", value=float(current_data.get('total_amount', 0)), key=f"a_{doc['id']}")
                    v_type = st.selectbox("Category", ["Invoice", "Receipt", "Bill", "Other"], index=0, key=f"t_{doc['id']}")
                
                with col2:
                    st.markdown("#### 🔍 Audit Insights")
                    v_results = validate_extraction(current_data)
                    for rule in v_results['rules']:
                        icon = "✅" if rule['status'] == "PASS" else ("⚠️" if rule['status'] == "WARNING" else "❌")
                        st.write(f"{icon} **{rule['rule']}**: {rule['message']}")
                    
                    st.markdown("---")
                    if st.button("✔️ Mark as Approved", key=f"app_{doc['id']}", use_container_width=True):
                        current_data['vendor_name'] = v_name
                        current_data['date'] = v_date
                        current_data['total_amount'] = v_amount
                        current_data['document_type'] = v_type
                        update_doc_status(doc['id'], "approved", current_data)
                        st.success("Validated successfully!")
                        st.rerun()

elif page == "Dashboard":
    st.title("📊 Operational Dashboard")
    df = get_data()
    
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Processed", len(df))
        c2.metric("Efficiency Rate", f"{round((len(df[df['status'] == 'approved']) / len(df)) * 100)}%", help="Auto-approved vs Total")
        c3.metric("Review Volume", len(df[df['status'] == 'needs_review']))
        c4.metric("Avg. Capture Confidence", f"{round(df['confidence'].mean())}%")
        
        st.markdown("---")
        st.write("### 📜 Processed Documents Ledger")
        # Visual color coding for statuses
        def color_status(val):
            color = "#d4edda" if val == "approved" else "#fff3cd"
            return f'background-color: {color}'
        
        st.dataframe(df.sort_values(by="timestamp", ascending=False).style.applymap(color_status, subset=['status']), use_container_width=True)
        
        st.markdown("---")
        # CSV Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Audit Trail (CSV)", data=csv, file_name=f"docuflow_audit_{time.strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
    else:
        st.info("No audit logs available. Start by uploading a document in the 'Upload' tab.")
