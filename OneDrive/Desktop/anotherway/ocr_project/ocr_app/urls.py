# ocr_app/urls.py
from django.urls import path
from .views import ocr_view

urlpatterns = [
    path('ocr/', ocr_view, name='ocr_view'),
]

# ocr_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ocr_app.urls')),
]
