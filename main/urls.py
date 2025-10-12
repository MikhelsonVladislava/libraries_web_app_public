"""URL для приложения main"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


app_name = 'main'
urlpatterns = [
    # Поиск
    path('', views.home, name='home'),] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)