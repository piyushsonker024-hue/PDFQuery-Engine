from flask import Flask, request, jsonify
import os
from text_extractor import extract_text
from table_extractor import extract_tables
from image_extractor import extract_images_with_ocr
from gemini_q_a  import gemini_answer
from config import OUTPUT_DIR
import uuid
import json

app = Flask(__name__)
UPLOAD_FOLDER=r"C:\Users\hp\OneDrive\Desktop\pdf_output"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['pdf']
    filename = f"{uuid.uuid4()}.pdf"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    text = extract_text(path)
    tables = extract_tables(path)
    images = extract_images_with_ocr(path, os.path.join(OUTPUT_DIR, "images"))

    json_output = {
        "text": text,
        "tables": tables,
        "images": images
    }

    with open(os.path.join(OUTPUT_DIR, f"{filename}.json"), "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=2)

    return jsonify({"message": "File processed", "pdf_id": filename}), 200

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    pdf_id = data.get("pdf_id")
    question = data.get("question")

    try:
        with open(os.path.join(OUTPUT_DIR, f"{pdf_id}.json"), "r", encoding="utf-8") as f:
            pdf_data = json.load(f)
    except:
        return jsonify({"error": "PDF not found"}), 404

    context = pdf_data.get("text", "")
    answer = gemini_answer(context, question)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True, port=800)



