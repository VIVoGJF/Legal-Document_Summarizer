import sys
from pathlib import Path

base = Path.cwd()
sys.path.append(str(base))

from core.extraction import extract_text_from_pdf, extract_text_pages
from core.summarization import summarize_document


# Path to a sample PDF
pdf_file = base / "data" / "input_docs" / "kiit_doc.pdf"

# Extract text (using your extraction function)
text = extract_text_from_pdf(pdf_file)

# Summarize with OpenAI
summary = summarize_document(text)

print("\n--- SUMMARY ---\n")
print(summary)
