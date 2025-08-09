from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    path('', views.home, name='home'),  # Home page for empty path
    path('books/', views.list_books, name='list_books'),  # Function-based view for listing books
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Class-based view for library details
]