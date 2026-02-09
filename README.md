# 📑 DocuFlow AI: Intelligent Document Processing

**DocuFlow AI** is a lightweight, high-performance web application designed to automate the extraction of structured data from invoices and receipts. Built for efficiency and cost-effectiveness, it leverages Large Language Models (LLMs) to transform messy document text into actionable business intelligence.

---

## 🚀 Core Features

-   **AI-Powered Extraction**: Uses OpenAI's latest models to extract invoice numbers, dates, vendors, line items, and totals.
-   **Intelligent Validation**: Built-in business rules automatically flag documents with missing data or low confidence scores.
-   **Manual Review Queue**: A dedicated workflow for human-in-the-loop verification of flagged documents.
-   **Operational Dashboard**: Real-time visualization of processing efficiency, volume, and data accuracy.
-   **Demo Mode**: A stable, key-free environment for presentations and interviews using pre-validated mock data.

## 🛠️ Technology Stack

-   **Frontend & Dashboard**: [Streamlit](https://streamlit.io/) (Python)
-   **AI Orchestration**: [OpenAI API](https://openai.com/) (GPT-4o-mini & GPT-4.1-nano)
-   **PDF Processing**: `pdfplumber`
-   **Data Storage**: CSV-based persistence for rapid prototyping and zero-dependency deployments.
-   **Document Generation**: `reportlab` (for generating test samples).

---

## 📂 Project Structure

```text
├── app.py                # Main Streamlit application entry point
├── start.sh              # Production-ready startup script with environment injection
├── utils/
│   ├── ai_extractor.py   # AI logic with automatic model fallback
│   ├── pdf_processor.py  # PDF text extraction engine
│   ├── validator.py      # Business rule engine
│   └── confidence.py     # Status calculation & confidence scoring
├── public_samples/       # Pre-generated valid PDF samples for testing
├── documents_data.csv    # Local data store (ledger)
└── requirements.txt      # Python dependencies
```

---

## ⚙️ Local Setup

1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd DocuFlow_AI
    ```

2.  **Install Dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create an `api.env` file (or use `start.sh`) with your OpenAI key:
    ```text
    OPENAI_API_KEY=your_key_here
    ```

4.  **Run the App**:
    ```bash
    ./start.sh
    ```

---

## 🌐 Online Deployment (Interviewer Guide)

The easiest way to share a live demo of this project is via **Streamlit Community Cloud**:

1.  **GitHub**: Push this codebase to a public/private GitHub repository.
2.  **Deploy**: Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud).
3.  **Secrets**: In the Streamlit Cloud dashboard, go to **Settings > Secrets** and paste your API key:
    ```toml
    OPENAI_API_KEY = "your-sk-..."
    ```
4.  **Live URL**: Share the generated URL with the reviewer.

---

## 🧠 Why this Architecture?

-   **Speed-to-Value**: Bypasses heavy database setups in favor of a robust CSV ledger, perfect for a high-impact portfolio piece.
-   **Model Fallback**: Implements a prioritized model list (Nano -> Mini) to ensure extraction never fails due to specific model outages.
-   **Clean Separation**: Modular utility structure allows for easy expansion (e.g., adding OCR or accounting API integrations).

---
*Created as a high-impact portfolio project for AI/Full-Stack roles.*
