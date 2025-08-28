"""
Advanced filtering configurations for the API.

This module provides custom filter classes and configurations for enhancing
the filtering capabilities of the Django REST Framework API.
"""

import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Advanced filtering class for Book model with custom filter methods.
    
    Provides comprehensive filtering options including:
    - Title filtering (exact, contains, starts with)
    - Author filtering (by name or ID)
    - Publication year filtering (exact, range, before/after)
    - Custom search across multiple fields
    """
    
    # Title filters
    title = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        help_text='Filter by book title (case-insensitive partial match)'
    )
    title_exact = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='iexact',
        help_text='Filter by exact book title (case-insensitive)'
    )
    title_starts_with = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='istartswith',
        help_text='Filter by books whose title starts with the given text'
    )
    
    # Author filters
    author_name = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive partial match)'
    )
    author_id = django_filters.NumberFilter(
        field_name='author__id',
        help_text='Filter by specific author ID'
    )
    
    # Publication year filters
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text='Filter by exact publication year'
    )
    year_after = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gt',
        help_text='Filter books published after this year'
    )
    year_before = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lt',
        help_text='Filter books published before this year'
    )
    year_range = django_filters.RangeFilter(
        field_name='publication_year',
        help_text='Filter books within a year range (e.g., year_range_min=1990&year_range_max=2000)'
    )
    
    # Decade filter
    decade = django_filters.ChoiceFilter(
        method='filter_by_decade',
        choices=[
            ('1900s', '1900-1909'),
            ('1910s', '1910-1919'),
            ('1920s', '1920-1929'),
            ('1930s', '1930-1939'),
            ('1940s', '1940-1949'),
            ('1950s', '1950-1959'),
            ('1960s', '1960-1969'),
            ('1970s', '1970-1979'),
            ('1980s', '1980-1989'),
            ('1990s', '1990-1999'),
            ('2000s', '2000-2009'),
            ('2010s', '2010-2019'),
            ('2020s', '2020-2029'),
        ],
        help_text='Filter books by decade of publication'
    )
    
    # Multi-field search
    search = django_filters.CharFilter(
        method='filter_search',
        help_text='Search across title and author name'
    )
    
    # Advanced filters
    has_multiple_books_by_author = django_filters.BooleanFilter(
        method='filter_prolific_authors',
        help_text='Filter books by authors who have written multiple books'
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'author': ['exact'],
            'publication_year': ['exact', 'lt', 'gt', 'range'],
        }
    
    def filter_by_decade(self, queryset, name, value):
        """
        Custom filter method to filter books by decade.
        """
        if not value:
            return queryset
        
        # Extract decade start year
        decade_start = int(value[:4])
        decade_end = decade_start + 9
        
        return queryset.filter(
            publication_year__gte=decade_start,
            publication_year__lte=decade_end
        )
    
    def filter_search(self, queryset, name, value):
        """
        Custom search method that searches across multiple fields.
        """
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(author__name__icontains=value)
        )
    
    def filter_prolific_authors(self, queryset, name, value):
        """
        Filter books by authors who have written multiple books.
        """
        if not value:
            return queryset
        
        from django.db.models import Count
        prolific_authors = Author.objects.annotate(
            book_count=Count('books')
        ).filter(book_count__gt=1)
        
        return queryset.filter(author__in=prolific_authors)


class AuthorFilter(django_filters.FilterSet):
    """
    Filtering class for Author model.
    """
    
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive partial match)'
    )
    
    name_starts_with = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
        help_text='Filter authors whose name starts with the given text'
    )
    
    has_books = django_filters.BooleanFilter(
        method='filter_has_books',
        help_text='Filter authors who have written books'
    )
    
    book_count_min = django_filters.NumberFilter(
        method='filter_book_count_min',
        help_text='Filter authors with at least this many books'
    )
    
    class Meta:
        model = Author
        fields = ['name']
    
    def filter_has_books(self, queryset, name, value):
        """
        Filter authors who have or haven't written books.
        """
        if value:
            return queryset.filter(books__isnull=False).distinct()
        else:
            return queryset.filter(books__isnull=True)
    
    def filter_book_count_min(self, queryset, name, value):
        """
        Filter authors with at least the specified number of books.
        """
        if not value:
            return queryset
        
        from django.db.models import Count
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
