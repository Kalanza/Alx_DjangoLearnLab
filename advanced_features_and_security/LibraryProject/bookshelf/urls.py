"""
URL configuration for the bookshelf application.
Includes secure routing and CSP reporting endpoint.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Book management URLs with secure patterns
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Example secure form demonstration
    path('example-form/', views.example_form_view, name='example_form'),
    
    # Security reporting endpoint
    path('csp-report/', views.csp_report, name='csp_report'),
]
