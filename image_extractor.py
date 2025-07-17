import fitz  
import pytesseract
from PIL import Image
import io
import os
import cv2
import numpy as np

def preprocess_table_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        11, 4
    )
    return Image.fromarray(thresh)

def extract_images_with_ocr(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    image_data = []

    os.makedirs(output_dir, exist_ok=True)

    for i, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image = Image.open(io.BytesIO(base_image["image"]))
            
            image_name = f"page_{i+1}_img_{img_index+1}.png"
            path = os.path.join(output_dir, image_name)
            image.save(path)

            processed_image = preprocess_table_image(image)

        
            ocr_text = pytesseract.image_to_string(processed_image, config="--psm 6")

            image_data.append({
                "page": i + 1,
                "image": image_name,
                "ocr_text": ocr_text.strip()
            })

    return image_data
