from pathlib import Path
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import yaml
from PIL import Image

# -------------------------
# Load config.yaml
# -------------------------
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Apply Tesseract config if available
if config.get("tesseract_cmd"):
    pytesseract.pytesseract.tesseract_cmd = config["tesseract_cmd"]

# Poppler path for pdf2image
POPLER_PATH = config.get("poppler_path") or None


def _ocr_page_image(img: Image.Image) -> str:
    """Run pytesseract OCR on a PIL Image and return text (str)."""
    return pytesseract.image_to_string(img)


def extract_text_pages(pdf_path: str, use_ocr: bool = True) -> list[str]:
    """
    Extract text per page from PDF.

    Returns: list of strings, one entry per page (empty string if nothing found).
    - First tries pdfplumber (selectable text).
    - If no text and use_ocr=True, runs OCR on that page.
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_file}")

    pages_text: list[str] = []

    # First attempt: extract with pdfplumber page-by-page
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
            pages_text.append(text)

    # If OCR requested, run OCR for pages with no/low text
    if use_ocr:
        for idx, page_text in enumerate(pages_text):
            if not page_text.strip() or len(page_text.strip()) < 10:
                page_number = idx + 1
                try:
                    images = convert_from_path(
                        str(pdf_file),
                        dpi=300,
                        first_page=page_number,
                        last_page=page_number,
                        poppler_path=POPLER_PATH,
                    )
                    if images:
                        ocr_text = _ocr_page_image(images[0])
                        pages_text[idx] = page_text + "\n" + ocr_text.strip()
                except Exception as e:
                    print(f"[OCR] Failed on page {page_number}: {e}")

    return [p.strip() for p in pages_text]


def extract_text_from_pdf(pdf_path: str, use_ocr: bool = True) -> str:
    """
    Convenience wrapper that returns full text (joined with page markers).
    """
    pages = extract_text_pages(pdf_path, use_ocr=use_ocr)

    if not pages:
        return "No readable text found."

    joined = []
    for i, p in enumerate(pages, start=1):
        joined.append(f"\n--- Page {i} ---\n{p}")
    return "\n".join(joined).strip()

