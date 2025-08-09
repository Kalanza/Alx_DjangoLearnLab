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
    # USER AUTHENTICATION URL PATTERNS
    # ========================================================================
    # These URLs link to the authentication views defined in views.py
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # User login using LoginView
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),  # User logout using LogoutView
    path('register/', views.register, name='register'),  # User registration using register function
]