# PDFQueryEngine

PDFQueryEngine is an end-to-end AI-powered PDF content analyzer that extracts text, tables, and image-based content using OCR, then answers user questions about the content using Gemini 1.5 Flash.

## Features

- Upload PDF with text, tables, or image-based data  
- Extracts and stores structured content (text, tables, images)  
- Ask questions based on uploaded PDF using Gemini AI  
- Download answers in CSV and JSON formats  
- Works with scanned PDFs via OCR  
- Modular backend using Flask; frontend using Streamlit

## Tech Stack

| Component       | Technology             |
|----------------|------------------------|
| Frontend       | Streamlit              |
| Backend        | Flask API              |
| OCR            | Tesseract / EasyOCR    |
| NLP/QA Model   | Gemini 1.5 Flash       |
| PDF Parsing    | PyMuPDF / pdfplumber   |

## Project Structure

```
PDFQueryEngine/
│
├── app.py                  # Streamlit frontend
├── backendapp.py           # Flask backend API
├── text_extractor.py       # Extracts text from PDF
├── table_extractor.py      # Extracts tables
├── image_extractor.py      # OCR on PDF images
├── gemini_q_a.py           # Gemini-powered Q&A
├── config.py               # Path config like OUTPUT_DIR
└── requirements.txt        # Python dependencies
```

## How It Works

### 1. Upload PDF  
User uploads a PDF via Streamlit UI → `/upload` API endpoint stores the PDF, extracts content, and saves it as JSON.

### 2. Ask a Question  
User inputs a question → `/ask` endpoint loads the extracted data and uses Gemini to answer based on context.

### 3. Download Results  
Output (question + answer + PDF ID) can be downloaded as CSV or JSON.

## Setup Instructions

### Prerequisites

- Python 3.10+
- Gemini API key (for `gemini_q_a.py`)
- Tesseract (for OCR)

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

### Install Requirements

```bash
pip install -r requirements.txt
```

## Run the Application

### 1. Start Flask Backend

```bash
python backendapp.py
```

### 2. Start Streamlit Frontend

```bash
streamlit run app.py
```

## Sample Usage

1. Upload a PDF via browser.
2. Click Process PDF to extract data.
3. Type a question like "What is the invoice total?" or "Who is the customer?"
4. Click Get Answer
5. Download your response.

## Output Format

Each processed PDF generates:

```json
{
  "text": "...",
  "tables": [...],
  "images": [...]
}
```

Answers are returned like:

```json
{
  "pdf_id": "...",
  "question": "...",
  "answer": "..."
}
```

## Notes

- Backend saves processed JSON in the directory defined in `config.py`
- You must provide your own implementation of:
  - `extract_text(path)`
  - `extract_tables(path)`
  - `extract_images_with_ocr(path, output_path)`
  - `gemini_answer(context, question)`

## Author

Piyush Sonker
