from django.urls import path
from .views import ExtractInvoiceAPIView

urlpatterns = [
    path('extract/', ExtractInvoiceAPIView.as_view(), name='extract_invoice'),
]
