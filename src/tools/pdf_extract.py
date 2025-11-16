import pymupdf as fitz
from pdf2image import convert_from_path
import pytesseract
from typing import List, Dict

def extract_pdf_text(path: str) -> List[Dict]:
    """
    Returns a list of pages: [{'page': i, 'text': '...'}]
    If page has no text, uses OCR (pytesseract).
    """
    doc = fitz.open(path)
    pages = []
    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = str(page.get_text("text")).strip()
        if not text:
            # render page to image for OCR
            pil_images = convert_from_path(path, first_page=i+1, last_page=i+1, dpi=200)
            if pil_images:
                text = pytesseract.image_to_string(pil_images[0], lang='por')  # Portuguese
                text = text.strip()
        pages.append({"page": i+1, "text": text})
    return pages
