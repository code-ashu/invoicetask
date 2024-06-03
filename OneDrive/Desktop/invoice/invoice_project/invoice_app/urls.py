from django.urls import path
from .views import InvoiceOCRView

urlpatterns = [
    path('invoice-ocr/', InvoiceOCRView.as_view(), name='invoice_ocr'),
]