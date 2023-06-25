from django.urls import path, include
from main import urls as main_urls

urlpatterns = [
    path('', include(main_urls)),
]