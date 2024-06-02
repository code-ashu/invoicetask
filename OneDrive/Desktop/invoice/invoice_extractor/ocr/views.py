# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import PDFUploadSerializer
# from pdf2image import convert_from_path
# import pytesseract
# import os

# class ExtractInvoiceAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = PDFUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             pdf_file = serializer.validated_data['pdf_file']

#             # Save the PDF file temporarily
#             with open('temp.pdf', 'wb') as temp_pdf:
#                 for chunk in pdf_file.chunks():
#                     temp_pdf.write(chunk)

#             # Convert PDF to images
#             images = convert_from_path('temp.pdf')

#             # Extract text from images
#             extracted_text = ""
#             for image in images:
#                 text = pytesseract.image_to_string(image)
#                 extracted_text += text + "\n"

#             # Clean up the temporary PDF file
#             os.remove('temp.pdf')

#             return Response({'extracted_text': extracted_text}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PDFUploadSerializer
from pdf2image import convert_from_path
import pytesseract
import os

class ExtractInvoiceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['pdf_file']

            # Save the PDF file temporarily
            temp_pdf_path = 'temp.pdf'
            with open(temp_pdf_path, 'wb') as temp_pdf:
                for chunk in pdf_file.chunks():
                    temp_pdf.write(chunk)

            try:
                # Convert PDF to images
                images = convert_from_path(temp_pdf_path)

                # Extract text from images
                extracted_text = ""
                for image in images:
                    text = pytesseract.image_to_string(image)
                    extracted_text += text + "\n"

                return Response({'extracted_text': extracted_text}, status=status.HTTP_200_OK)
            finally:
                # Clean up the temporary PDF file
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
