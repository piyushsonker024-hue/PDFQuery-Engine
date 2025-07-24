import os
from dotenv import load_dotenv
load_dotenv()

POPPLER_PATH = r"C:\Users\hp\OneDrive\Desktop\chatwithpdf\poppler-24.08.0\Library\bin"
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OUTPUT_DIR = r"C:\Users\hp\OneDrive\Desktop\pdf_output"
GEMINI_API_KEY =os.getenv("GEMINI_API_KEY")

