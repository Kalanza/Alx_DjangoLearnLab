# ============================================================================
# RELATIONSHIP APP URL PATTERNS
# ============================================================================
# This module defines URL patterns for the relationship_app Django application
# including library management URLs and user authentication URLs
# ============================================================================

from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # ========================================================================
    # LIBRARY MANAGEMENT URL PATTERNS
    # ========================================================================
    path('', views.home, name='home'),  # Home page for empty path
    path('books/', views.list_books, name='list_books'),  # Function-based view for listing books
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Class-based view for library details
    
    # ========================================================================
    # CUSTOM PERMISSIONS URL PATTERNS - SECURED BOOK OPERATIONS
    # ========================================================================
    path('books/add/', views.add_book, name='add_book'),  # Add book - requires can_add_book permission
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),  # Edit book - requires can_change_book permission
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),  # Delete book - requires can_delete_book permission
    
    # ========================================================================
    # USER AUTHENTICATION URL PATTERNS
    # ========================================================================
    # These URLs link to the authentication views defined in views.py
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # User login using LoginView
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),  # User logout using LogoutView
    path('register/', views.register, name='register'),  # User registration using register function
    path('admin_dashboard/', views.admin_view, name='admin_dashboard'),
    path('librarian_dashboard/', views.librarian_view, name='librarian_dashboard'),
    path('member_dashboard/', views.member_view, name='member_dashboard'),
]