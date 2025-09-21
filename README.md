# 📑 AI Legal Document Summarizer & Analyzer

An AI-powered tool to **extract, analyze, and summarize legal documents**.  
It combines **OCR, NLP (spaCy, Regex), and Gemini LLM** to deliver structured insights such as **parties, dates, obligations, money/penalties, risks, and suggestions**.  
A **Streamlit web app** provides an interactive interface to upload legal documents (PDF), view analysis results, and download a formatted PDF report.

---

## ✨ Features

- **Text Extraction**  
  - Extracts text from PDFs using `pdfplumber` and OCR (`pytesseract + pdf2image`).  

- **Entity Extraction**  
  - Detects Parties, Dates/Times, Money/Penalties, Obligations.  
  - Uses **spaCy + Regex** rules.  

- **Risk Analysis**  
  - Identifies legal risks such as termination clauses, confidentiality breaches, liabilities, dispute resolution, etc.  

- **AI-Enhanced Summarization**  
  - Refines summary, entities, and risks using **Gemini LLM**.  
  - Grammar correction + structured **JSON** output.  

- **Web App (Streamlit)**  
  - Upload legal PDF documents.  
  - Get structured AI-enhanced analysis (summary, parties, dates, risks, etc.).  
  - Export results as a professional **PDF report**.  
  - Re-upload new documents seamlessly.  

---

## 📂 Project Structure

```
legal-doc-analyzer/
│── core/
│   ├── extraction.py       # PDF text extraction (OCR + pdfplumber)
│   ├── entities.py         # Entity extraction (Parties, Dates, Money, Obligations)
│   ├── risks.py            # Risk analysis using keyword patterns
│   ├── summarization.py    # Summarization + Gemini AI enhancement
│   ├── pdf_writer.py       # Generate professional PDF reports
│── data/
│   ├── input_docs/         # Place input PDFs here
│   ├── output_docs/        # Generated reports saved here
│── tests/
│   ├── test_extraction.ipynb
│   ├── test_entities.ipynb
│   ├── test_risks.ipynb
│   ├── test_summarization.ipynb
│── app.py                  # Streamlit web app
│── config.yaml             # Config (paths, models, etc.)
│── requirements.txt        # Python dependencies
│── README.md               # 📍 Project documentation
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/legal-doc-analyzer.git
cd legal-doc-analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```


## 📊 Example Output


### Upload Page
![Upload Document](asset\upload.png)

### Final Analysis Output
![Final Analysis](asset\analysis.png)


---

## 🛠 Tech Stack

- **Python**
- **Streamlit** – Interactive web app
- **pdfplumber, pdf2image, pytesseract** – Text extraction & OCR
- **spaCy, Regex** – Entity extraction
- **Gemini LLM (Google GenAI)** – Summarization & grammar correction
- **ReportLab** – PDF generation

---

## 🚀 Future Improvements

- Add **multi-language support** for contracts.  
- Support **clause-level risk scoring**.  
- Enable **bulk PDF processing**.  
- Integrate **vector search for precedent case laws**.  

---

