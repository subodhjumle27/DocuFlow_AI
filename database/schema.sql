-- Table: documents
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_size INTEGER,
    file_hash TEXT,
    status TEXT CHECK(status IN ('processing', 'approved', 'needs_review', 'rejected')),
    overall_confidence REAL,
    processing_time_seconds REAL,
    pdf_text TEXT
);

-- Table: extracted_data
CREATE TABLE IF NOT EXISTS extracted_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER REFERENCES documents(id),
    document_type TEXT,
    invoice_number TEXT,
    date TEXT,
    vendor_name TEXT,
    total_amount REAL,
    currency TEXT,
    tax_amount REAL,
    payment_terms TEXT,
    line_items_json TEXT,
    confidence_scores_json TEXT,
    validation_results_json TEXT
);

-- Table: audit_log
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER REFERENCES documents(id),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    action TEXT,
    details TEXT,
    user_id TEXT DEFAULT 'system'
);
