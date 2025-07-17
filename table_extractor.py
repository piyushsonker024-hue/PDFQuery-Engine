import camelot
import fitz  
import os

def preprocess_pdf_pages(pdf_path, output_dir, dpi=300):

    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)
    image_pdfs = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        image_path = os.path.join(output_dir, f"page_{i+1}.png")
        pdf_path_out = os.path.join(output_dir, f"page_{i+1}.pdf")
        pix.save(image_path)

        
        img_doc = fitz.open()  
        img_page = img_doc.new_page(width=pix.width, height=pix.height)
        img_page.insert_image(img_page.rect, filename=image_path)
        img_doc.save(pdf_path_out)
        img_doc.close()

        image_pdfs.append(pdf_path_out)
    
    return image_pdfs
def extract_tables(pdf_path, preprocess=True):
    temp_dir = "temp_pages"
    extracted_tables = []

    if preprocess:
        image_pdfs = preprocess_pdf_pages(pdf_path, temp_dir)
        for image_pdf in image_pdfs:
            tables = camelot.read_pdf(image_pdf, flavor='lattice', strip_text='\n')
            for table in tables:
                extracted_tables.append(table.df.to_dict(orient='records'))
    else:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice', strip_text='\n')
        extracted_tables = [table.df.to_dict(orient='records') for table in tables]

    return extracted_tables

