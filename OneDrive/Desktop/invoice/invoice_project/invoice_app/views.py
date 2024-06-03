
import pytesseract
from pdf2image import convert_from_bytes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PDFUploadSerializer
import re

class InvoiceOCRView(APIView):
    def post(self, request):
        serializer = PDFUploadSerializer(data=request.data)
        if serializer.is_valid():
            pdf_files = serializer.validated_data['files']
            all_invoices_data = []

            for pdf_file in pdf_files:
                pages = convert_from_bytes(pdf_file.read())

                extracted_text = ""
                for page in pages:
                    text = pytesseract.image_to_string(page)
                    extracted_text += text + "\n"
                
                invoice_data = self.extract_invoice_data(extracted_text)
                all_invoices_data.append(invoice_data)
            
            return Response(all_invoices_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def extract_invoice_data(self, text):
        invoice_number_pattern = r'Invoice No\s*:\s*([A-Z0-9]+)'
        date_pattern = r'Date\s*:\s*([\d/]+)'
        total_amount_pattern = r'Total Amount Chargeable\s*:\s*([\d,]+\.\d{2})'
        gstin_pattern = r'GSTIN\s*:\s*([A-Z0-9]+)'
        vendor_code_pattern = r'Vendor Code\s*:\s*([A-Z0-9]+)'
        total_invoice_value_pattern = r'Total Invoice Value in Figure\s*:\s*([\d,]+\.\d{2})'
        cin_pattern = r'CIN\s*:\s*([A-Z0-9]+)'
        hsn_no_pattern = r'H\.S\.N No\s*:\s*([A-Z0-9]+)'
        po_no_pattern = r'P O No\s*:\s*([A-Z0-9]+)'
        hsn_sac_code_pattern = r'HSN/SAC Code\s*:\s*([A-Z0-9]+)'
        assessable_value_pattern = r'Assessable Value \( per Unit Rs\.\)\s*:\s*([\d,]+\.\d{2})'
        total_assessable_value_pattern = r'Total Assessable Value Rs\.\s*:\s*([\d,]+\.\d{2})'
        total_qty_of_goods_pattern = r'Total Qty of Goods\s*:\s*([\d,]+\.\d{2})'

        invoice_number = re.search(invoice_number_pattern, text)
        date = re.search(date_pattern, text)
        total_amount = re.search(total_amount_pattern, text)
        gstin = re.search(gstin_pattern, text)
        vendor_code = re.search(vendor_code_pattern, text)
        total_invoice_value = re.search(total_invoice_value_pattern, text)
        cin = re.search(cin_pattern, text)
        hsn_no = re.search(hsn_no_pattern, text)
        po_no = re.search(po_no_pattern, text)
        hsn_sac_code = re.search(hsn_sac_code_pattern, text)
        assessable_value = re.search(assessable_value_pattern, text)
        total_assessable_value = re.search(total_assessable_value_pattern, text)
        total_qty_of_goods = re.search(total_qty_of_goods_pattern, text)

        invoice_data = {
            'invoice_number': invoice_number.group(1) if invoice_number else None,
            'date': date.group(1) if date else None,
            'total_amount_chargeable': total_amount.group(1) if total_amount else None,
            'gstin': gstin.group(1) if gstin else None,
            'vendor_code': vendor_code.group(1) if vendor_code else None,
            'total_invoice_value': total_invoice_value.group(1) if total_invoice_value else None,
            'cin': cin.group(1) if cin else None,
            'hsn_no': hsn_no.group(1) if hsn_no else None,
            'po_no': po_no.group(1) if po_no else None,
            'hsn_sac_code': hsn_sac_code.group(1) if hsn_sac_code else None,
            'assessable_value': assessable_value.group(1) if assessable_value else None,
            'total_assessable_value': total_assessable_value.group(1) if total_assessable_value else None,
            'total_qty_of_goods': total_qty_of_goods.group(1) if total_qty_of_goods else None,
        }
        return invoice_data
