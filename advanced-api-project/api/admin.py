from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Author model.
    """
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.
    """
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering = ['title']
