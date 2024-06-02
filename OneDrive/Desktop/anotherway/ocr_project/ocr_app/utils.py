import fitz  # PyMuPDF
import pytesseract
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        text += pytesseract.image_to_string(pix.tobytes(), lang='eng')
    return text

# Correctly specify the PDF file path
pdf_path = r'C:\Users\Lenovo\OneDrive\Desktop\temp.pdf'
text = extract_text_from_pdf(pdf_path)

# Clean up the uploaded file
os.remove(pdf_path)

# Return the text as a JSON response
from django.http import JsonResponse
response = JsonResponse({'text': text})
