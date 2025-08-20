"""
Django forms for the bookshelf application.
These forms provide built-in security features including input validation,
CSRF protection, and safe handling of user data.
"""
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Book
import datetime


class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books.
    Uses Django's ModelForm for automatic validation and security features.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': 200,
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': 100,
                'required': True
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'required': True
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom validation
        current_year = datetime.datetime.now().year
        self.fields['publication_year'].validators = [
            MinValueValidator(1000, message="Publication year must be after 1000"),
            MaxValueValidator(current_year, message=f"Publication year cannot be in the future (after {current_year})")
        ]
    
    def clean_title(self):
        """
        Custom validation for title field.
        Prevents XSS by sanitizing input and ensuring proper length.
        """
        title = self.cleaned_data.get('title')
        if title:
            # Remove any potentially harmful characters
            title = title.strip()
            if len(title) < 2:
                raise forms.ValidationError("Title must be at least 2 characters long.")
            # Additional security: prevent HTML/script injection
            if '<' in title or '>' in title or 'script' in title.lower():
                raise forms.ValidationError("Title contains invalid characters.")
        return title
    
    def clean_author(self):
        """
        Custom validation for author field.
        """
        author = self.cleaned_data.get('author')
        if author:
            author = author.strip()
            if len(author) < 2:
                raise forms.ValidationError("Author name must be at least 2 characters long.")
            # Additional security: prevent HTML/script injection
            if '<' in author or '>' in author or 'script' in author.lower():
                raise forms.ValidationError("Author name contains invalid characters.")
        return author


class BookSearchForm(forms.Form):
    """
    Secure search form for books.
    Provides safe handling of search queries to prevent SQL injection.
    """
    search_query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books by title or author...',
            'autocomplete': 'off'
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All Fields'),
            ('title', 'Title'),
            ('author', 'Author'),
            ('year', 'Publication Year')
        ],
        required=False,
        initial='all',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean_search_query(self):
        """
        Sanitize search query to prevent XSS and injection attacks.
        """
        query = self.cleaned_data.get('search_query')
        if query:
            query = query.strip()
            # Remove potentially harmful characters
            if '<' in query or '>' in query or 'script' in query.lower():
                raise forms.ValidationError("Search query contains invalid characters.")
            # Limit length to prevent DoS attacks
            if len(query) > 200:
                raise forms.ValidationError("Search query is too long.")
        return query
