# ocr_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .utils import extract_text_from_pdf
import os

def ocr_view(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        file_path = os.path.join('uploads', pdf_file.name)
        
        with open('C:\Users\Lenovo\OneDrive\Desktop\temp.pdf', 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)
        
        text = extract_text_from_pdf('C:\Users\Lenovo\OneDrive\Desktop\temp.pdf')
        os.remove('C:\Users\Lenovo\OneDrive\Desktop\temp.pdf')  # Clean up the uploaded file
        return JsonResponse({'text': text})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
