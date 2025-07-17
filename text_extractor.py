import fitz
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from config import POPPLER_PATH, TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ''.join(page.get_text() for page in doc)
        if len(text.strip()) > 50:
            return text
    except:
        pass
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    return ''.join(pytesseract.image_to_string(img.convert('L')) for img in pages)
