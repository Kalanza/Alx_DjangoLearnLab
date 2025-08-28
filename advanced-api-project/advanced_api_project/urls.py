"""
URL configuration for advanced_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

This configuration includes:
- Admin interface at /admin/
- API endpoints at /api/ (includes all book and author CRUD operations)
- Custom endpoints for advanced functionality

API Endpoints Available:
- /api/authors/ - Author list and creation
- /api/authors/<id>/ - Individual author operations
- /api/books/ - Book listing with filtering
- /api/books/create/ - Book creation
- /api/books/<id>/ - Book detail view
- /api/books/<id>/update/ - Book update
- /api/books/<id>/delete/ - Book deletion
- /api/books/update/ - Book update (alternative pattern)
- /api/books/delete/ - Book deletion (alternative pattern)
- /api/books/by-author/<author_id>/ - Books by specific author
- /api/books/statistics/ - Book statistics
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # Include API URLs with all CRUD operations
]
