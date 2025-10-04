"""
URL configuration for bookshelf app with permission-protected views
"""
from django.urls import path
from . import views

urlpatterns = [
    # Book management URLs with permission requirements
    path('books/', views.book_list, name='book_list'),           # Requires: can_view
    path('books/create/', views.book_create, name='book_create'), # Requires: can_create  
    path('books/<int:book_id>/edit/', views.book_edit, name='book_edit'), # Requires: can_edit
    path('books/<int:book_id>/delete/', views.book_delete, name='book_delete'), # Requires: can_delete
    
    # Utility URL for testing permissions
    path('permissions/', views.user_permissions_view, name='user_permissions'),
]