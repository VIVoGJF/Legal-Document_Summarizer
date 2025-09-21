import streamlit as st
from pathlib import Path
import json
from core.extraction import extract_text_from_pdf
from core.entities import extract_entities
from core.risks import analyze_risks
from core.summarization import summarize_document
from core.pdf_writer import save_json_to_pdf

st.set_page_config(page_title="AI Legal Document Analyzer", layout="wide")

# -----------------------
# Session state setup
# -----------------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "json_result" not in st.session_state:
    st.session_state.json_result = None
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None


def reset_app():
    st.session_state.analysis_done = False
    st.session_state.json_result = None
    st.session_state.pdf_path = None


st.title("📑 AI Legal Document Summarizer")

# -----------------------
# Upload stage (cozy centered box)
# -----------------------
if not st.session_state.analysis_done:
    st.markdown(
        """
        <style>
        .upload-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 5vh;
        }
        .upload-box {
            border: 2px dashed #6c63ff;
            border-radius: 15px;
            padding: 40px;
            width: 60%;
            text-align: center;
            background-color: #1e1e1e;
            transition: 0.3s ease;
        }
        .upload-box:hover {
            background-color: #2c2c2c;
            border-color: #8a85ff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="upload-container">
            <h2>📤 Upload a Legal PDF Document</h2>
            <p>Drag & drop your file below, or click to browse</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        with st.spinner("⚙️ Analyzing document… please wait."):
            # Save uploaded file temporarily
            input_path = Path("data/input_docs") / uploaded_file.name
            input_path.parent.mkdir(parents=True, exist_ok=True)
            with open(input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Pipeline: Extract → Entities → Risks → Summarize
            text = extract_text_from_pdf(input_path, use_ocr=True)
            entities = extract_entities(text)
            risks = analyze_risks(text)
            json_result = summarize_document(text, entities, risks)

            # Save JSON result
            st.session_state.json_result = json.loads(json_result)

            # Save PDF
            pdf_path = Path("data/output_docs") / "analysis_report.pdf"
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            save_json_to_pdf(json_result, filename=str(pdf_path))
            st.session_state.pdf_path = pdf_path

            st.session_state.analysis_done = True
            st.rerun()



# -----------------------
# Analysis stage
# -----------------------
else:
    data = st.session_state.json_result

    st.subheader("✅ Final AI-Enhanced Analysis")

    # Display results in clean sections
    st.markdown("### 📝 Summary")
    st.write(data.get("summary", "Not available"))

    st.markdown("### ⭐ Parties")
    st.write(data.get("parties", "Not available"))

    st.markdown("### 📅 Dates / Time")
    st.markdown(data.get("date/time", "Not available"), unsafe_allow_html=True)

    st.markdown("### 💰 Money / Penalties")
    st.write(data.get("money/penalties", "Not available"))

    st.markdown("### 📌 Obligations")
    st.write(data.get("obligations", "Not available"))

    st.markdown("### ⚖️ Risks")
    st.markdown(data.get("risks", "Not available"), unsafe_allow_html=True)

    st.markdown("### 💡Suggestions")
    st.info(data.get("suggestion", "No suggestions provided."))

    with open(st.session_state.pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_bytes,
        file_name="legal_analysis.pdf",
        mime="application/pdf",
    )

    # Reset button
    st.button("🔄 Upload Another Document", on_click=reset_app)
