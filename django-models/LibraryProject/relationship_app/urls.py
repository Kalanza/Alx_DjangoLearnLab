# ============================================================================
# RELATIONSHIP APP URL PATTERNS
# ============================================================================
# This module defines URL patterns for the relationship_app Django application
# including library management URLs and user authentication URLs
# ============================================================================

from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    # ========================================================================
    # LIBRARY MANAGEMENT URL PATTERNS
    # ========================================================================
    path('', views.home, name='home'),  # Home page for empty path
    path('books/', views.list_books, name='list_books'),  # Function-based view for listing books
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Class-based view for library details
    
    # ========================================================================
    # USER AUTHENTICATION URL PATTERNS
    # ========================================================================
    # These URLs link to the authentication views defined in views.py
    path('login/', views.CustomLoginView.as_view(), name='login'),  # User login using custom LoginView
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),  # User logout using custom LogoutView
    path('register/', views.SignUpView.as_view(), name='register'),  # User registration using SignUpView
]