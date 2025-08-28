"""
URL Configuration for the API app.

This module defines URL patterns for all API endpoints, including:
- Author CRUD operations
- Book CRUD operations (separate views)
- Custom endpoints for advanced functionality
- Statistical and analytical endpoints

URL Patterns Structure:
- /authors/ - Author list and creation
- /authors/<id>/ - Individual author operations
- /books/ - Book listing with filtering
- /books/create/ - Book creation
- /books/<id>/ - Book detail view
- /books/<id>/update/ - Book update
- /books/<id>/delete/ - Book deletion
- /books/by-author/<author_id>/ - Books by specific author
- /books/statistics/ - Book statistics
"""

from django.urls import path
from . import views

# URL patterns for API endpoints
urlpatterns = [
    # =================================================================
    # AUTHOR ENDPOINTS
    # =================================================================
    
    # Authors list and create
    path(
        'authors/', 
        views.AuthorListCreateView.as_view(), 
        name='author-list-create'
    ),
    
    # Individual author operations (retrieve, update, delete)
    path(
        'authors/<int:pk>/', 
        views.AuthorDetailView.as_view(), 
        name='author-detail'
    ),
    
    # =================================================================
    # BOOK ENDPOINTS - Separate views for maximum flexibility
    # =================================================================
    
    # Books list with advanced filtering
    path(
        'books/', 
        views.BookListView.as_view(), 
        name='book-list'
    ),
    
    # Book creation (separate endpoint for clarity)
    path(
        'books/create/', 
        views.BookCreateView.as_view(), 
        name='book-create'
    ),
    
    # Book detail view (read-only)
    path(
        'books/<int:pk>/', 
        views.BookDetailView.as_view(), 
        name='book-detail'
    ),
    
    # Book update (separate endpoint)
    path(
        'books/<int:pk>/update/', 
        views.BookUpdateView.as_view(), 
        name='book-update'
    ),
    
    # Book deletion (separate endpoint)
    path(
        'books/<int:pk>/delete/', 
        views.BookDeleteView.as_view(), 
        name='book-delete'
    ),
    
    # =================================================================
    # CUSTOM ENDPOINTS - Advanced functionality
    # =================================================================
    
    # Books by specific author
    path(
        'books/by-author/<int:author_id>/', 
        views.BooksByAuthorView.as_view(), 
        name='books-by-author'
    ),
    
    # Book statistics (function-based view)
    path(
        'books/statistics/', 
        views.book_statistics, 
        name='book-statistics'
    ),
]
