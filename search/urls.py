"""URL для приложения search"""

from django.urls import path

from . import views


app_name = 'search'
urlpatterns = [
    # Поиск
    path('', views.search_request, name='search_request'),
    path('result/', views.search_list, name='search-list')]
