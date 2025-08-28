"""
Advanced API Views for Django REST Framework - Custom and Generic Views

This module demonstrates comprehensive usage of Django REST Framework's generic views,
custom view behavior, permissions, and filtering. It showcases different approaches
to handling CRUD operations with fine-tuned control over API behavior.

Features:
- Generic views for efficient CRUD operations
- Custom permission handling
- Query filtering and optimization
- Custom response formatting
- Detailed logging and error handling
"""

from rest_framework import generics, status, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter, AuthorFilter
import logging

# Set up logging
logger = logging.getLogger(__name__)


# =============================================================================
# AUTHOR VIEWS - Combined Generic Views
# =============================================================================

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    Enhanced author operations with filtering, searching, and ordering.
    
    Features:
    - GET: Returns paginated list of all authors with their nested books
    - POST: Creates a new author with validation
    - Advanced filtering by author name and book count
    - Search functionality by author name
    - Ordering by name and book count
    - Permission: IsAuthenticatedOrReadOnly - read access for all, create requires authentication
    
    Filtering Options:
    - name: Filter by author name (partial match)
    - name_starts_with: Filter by name prefix
    - has_books: Filter authors who have/haven't written books
    - book_count_min: Filter authors with minimum number of books
    
    Ordering Options:
    - name: Order by author name
    - book_count: Order by number of books written
    - Use '-' prefix for descending order
    
    Example URLs:
    - /api/authors/?name_starts_with=J&ordering=name
    - /api/authors/?has_books=true&ordering=-book_count
    - /api/authors/?book_count_min=2
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Using the specific permission class
    
    # Configure filtering, searching, and ordering backends
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Use custom filter class
    filterset_class = AuthorFilter
    
    # Search configuration
    search_fields = [
        'name',     # Search in author name
        '^name',    # Name starts with (higher priority)
        '=name',    # Exact name match (highest priority)
    ]
    
    # Ordering configuration
    ordering_fields = ['name', 'id']
    ordering = ['name']  # Default ordering
    
    def get_queryset(self):
        """
        Enhanced queryset with book count annotation for ordering.
        """
        queryset = super().get_queryset()
        
        # Add book count annotation for ordering and filtering
        queryset = queryset.annotate(
            book_count=Count('books')
        )
        
        # Optimize with prefetch_related for related books
        queryset = queryset.prefetch_related('books')
        
        return queryset
    
    def get_ordering(self):
        """
        Custom ordering to handle book_count ordering.
        """
        ordering = self.request.query_params.get('ordering')
        if ordering:
            # Handle book_count ordering
            if ordering in ['book_count', '-book_count']:
                return [ordering]
        
        return super().get_ordering()
    
    def perform_create(self, serializer):
        """
        Custom behavior when creating a new author.
        Logs the creation and can add additional business logic.
        """
        author = serializer.save()
        logger.info(f"New author created: {author.name} (ID: {author.id})")
        return author
    
    def list(self, request, *args, **kwargs):
        """
        Enhanced list method with additional response information.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'message': 'Authors retrieved successfully',
                'total_count': queryset.count(),
                'current_page_count': len(serializer.data),
                'filters_applied': self._get_applied_filters(request),
                'ordering_applied': request.query_params.get('ordering', 'name'),
                'search_query': request.query_params.get('search', None),
                'authors': serializer.data
            })
        
        # Non-paginated response
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Authors retrieved successfully',
            'total_count': queryset.count(),
            'filters_applied': self._get_applied_filters(request),
            'ordering_applied': request.query_params.get('ordering', 'name'),
            'search_query': request.query_params.get('search', None),
            'available_filters': self._get_available_filters(),
            'authors': serializer.data
        })
    
    def _get_applied_filters(self, request):
        """
        Get information about currently applied filters.
        """
        applied_filters = {}
        filter_params = ['name', 'name_starts_with', 'has_books', 'book_count_min', 'search']
        
        for param in filter_params:
            value = request.query_params.get(param)
            if value is not None:
                applied_filters[param] = value
        
        return applied_filters
    
    def _get_available_filters(self):
        """
        Provide information about available filtering options.
        """
        return {
            'text_filters': {
                'name': 'Filter by author name (partial match)',
                'name_starts_with': 'Filter by name prefix',
                'search': 'Search in author name'
            },
            'boolean_filters': {
                'has_books': 'Filter authors who have written books (true/false)'
            },
            'numeric_filters': {
                'book_count_min': 'Filter authors with at least this many books'
            },
            'ordering_options': {
                'name': 'Order by author name',
                'book_count': 'Order by number of books written',
                'note': 'Use "-" prefix for descending order'
            }
        }


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Individual author operations - retrieve, update, and delete.
    
    Features:
    - GET: Returns specific author with nested books
    - PUT/PATCH: Updates author information
    - DELETE: Removes author and cascades to books
    - Permission: IsAuthenticatedOrReadOnly - read access for all, modify/delete requires authentication
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Using the specific permission class
    
    def perform_update(self, serializer):
        """
        Custom update behavior with logging.
        """
        author = serializer.save()
        logger.info(f"Author updated: {author.name} (ID: {author.id})")
        return author
    
    def perform_destroy(self, instance):
        """
        Custom deletion behavior with logging.
        """
        author_name = instance.name
        author_id = instance.id
        instance.delete()
        logger.warning(f"Author deleted: {author_name} (ID: {author_id})")


# =============================================================================
# BOOK VIEWS - Separate Generic Views for Maximum Flexibility
# =============================================================================

class BookListView(generics.ListAPIView):
    """
    Advanced book listing with comprehensive filtering, searching, and ordering.
    
    Features:
    - GET: Returns paginated list of all books
    - Advanced filtering by title, author, publication year, decade
    - Multi-field search functionality
    - Flexible ordering capabilities
    - Custom filters for complex queries
    - Permission: Open access for reading
    
    Filtering Options:
    - title: Filter by book title (partial match)
    - title_exact: Filter by exact book title
    - title_starts_with: Filter by title prefix
    - author_name: Filter by author name (partial match)
    - author_id: Filter by specific author ID
    - publication_year: Filter by exact year
    - year_after: Books published after specified year
    - year_before: Books published before specified year
    - year_range: Books within year range (year_range_min, year_range_max)
    - decade: Filter by decade (1990s, 2000s, etc.)
    - search: Multi-field search across title and author
    - has_multiple_books_by_author: Books by prolific authors
    
    Ordering Options:
    - title: Order by book title
    - publication_year: Order by publication year
    - author__name: Order by author name
    - Use '-' prefix for descending order (e.g., -publication_year)
    
    Example URLs:
    - /api/books/?search=Harry&ordering=publication_year
    - /api/books/?author_name=Rowling&year_after=1990
    - /api/books/?decade=1990s&ordering=-publication_year
    - /api/books/?title_starts_with=The&has_multiple_books_by_author=true
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Configure filtering, searching, and ordering backends
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Use custom filter class for advanced filtering
    filterset_class = BookFilter
    
    # Additional simple filters (for backward compatibility)
    filterset_fields = ['author', 'publication_year']
    
    # Search configuration
    search_fields = [
        'title',           # Search in book title
        'author__name',    # Search in author name
        '^title',          # Title starts with (higher priority)
        '=title',          # Exact title match (highest priority)
    ]
    
    # Ordering configuration
    ordering_fields = [
        'title',
        'publication_year', 
        'author__name',
        'id'  # Allow ordering by ID for consistent pagination
    ]
    ordering = ['title']  # Default ordering
    
    def get_queryset(self):
        """
        Enhanced queryset with optimizations and additional filtering logic.
        """
        queryset = super().get_queryset()
        
        # Optimize query with select_related for foreign keys
        queryset = queryset.select_related('author')
        
        # Custom filter: Recently published books (last 10 years)
        recent_only = self.request.query_params.get('recent_only', None)
        if recent_only and recent_only.lower() == 'true':
            from datetime import date
            current_year = date.today().year
            queryset = queryset.filter(publication_year__gte=current_year - 10)
        
        # Custom filter: Classic books (published before 1950)
        classics_only = self.request.query_params.get('classics_only', None)
        if classics_only and classics_only.lower() == 'true':
            queryset = queryset.filter(publication_year__lt=1950)
        
        # Custom filter: Books with long titles
        long_titles_only = self.request.query_params.get('long_titles_only', None)
        if long_titles_only and long_titles_only.lower() == 'true':
            queryset = queryset.extra(where=["LENGTH(title) > 20"])
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Enhanced list response with comprehensive metadata and filtering information.
        """
        # Get the filtered queryset
        queryset = self.filter_queryset(self.get_queryset())
        
        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'message': 'Books retrieved successfully',
                'total_count': queryset.count(),
                'current_page_count': len(serializer.data),
                'filters_applied': self._get_applied_filters(request),
                'ordering_applied': request.query_params.get('ordering', 'title'),
                'search_query': request.query_params.get('search', None),
                'books': serializer.data
            })
        
        # Non-paginated response
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Books retrieved successfully',
            'total_count': queryset.count(),
            'filters_applied': self._get_applied_filters(request),
            'ordering_applied': request.query_params.get('ordering', 'title'),
            'search_query': request.query_params.get('search', None),
            'available_filters': self._get_available_filters(),
            'books': serializer.data
        })
    
    def _get_applied_filters(self, request):
        """
        Get information about currently applied filters.
        """
        applied_filters = {}
        
        # Check for each possible filter parameter
        filter_params = [
            'title', 'title_exact', 'title_starts_with',
            'author_name', 'author_id', 'author',
            'publication_year', 'year_after', 'year_before',
            'year_range_min', 'year_range_max', 'decade',
            'search', 'has_multiple_books_by_author',
            'recent_only', 'classics_only', 'long_titles_only'
        ]
        
        for param in filter_params:
            value = request.query_params.get(param)
            if value is not None:
                applied_filters[param] = value
        
        return applied_filters
    
    def _get_available_filters(self):
        """
        Provide information about available filtering options.
        """
        return {
            'text_filters': {
                'title': 'Filter by book title (partial match)',
                'title_exact': 'Filter by exact book title',
                'title_starts_with': 'Filter by title prefix',
                'author_name': 'Filter by author name (partial match)',
                'search': 'Search across title and author name'
            },
            'numeric_filters': {
                'author_id': 'Filter by specific author ID',
                'publication_year': 'Filter by exact publication year',
                'year_after': 'Books published after specified year',
                'year_before': 'Books published before specified year'
            },
            'special_filters': {
                'decade': 'Filter by decade (1990s, 2000s, etc.)',
                'has_multiple_books_by_author': 'Books by prolific authors',
                'recent_only': 'Books published in the last 10 years',
                'classics_only': 'Books published before 1950',
                'long_titles_only': 'Books with titles longer than 20 characters'
            },
            'ordering_options': {
                'title': 'Order by book title',
                'publication_year': 'Order by publication year',
                'author__name': 'Order by author name',
                'note': 'Use "-" prefix for descending order (e.g., -publication_year)'
            }
        }


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific book by ID.
    
    Features:
    - GET: Returns detailed book information
    - Includes author information
    - Permission: Open access for reading
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        """
        Custom retrieve with additional context.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Add related books by the same author
        related_books = Book.objects.filter(
            author=instance.author
        ).exclude(id=instance.id).select_related('author')
        
        return Response({
            'message': 'Book retrieved successfully',
            'book': serializer.data,
            'related_books_by_author': BookSerializer(related_books, many=True).data
        })


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book with enhanced validation and logging.
    
    Features:
    - POST: Creates a new book with custom validation
    - Requires authentication
    - Detailed validation error handling
    - Creation logging
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Using the specific permission class
    
    def perform_create(self, serializer):
        """
        Custom creation behavior with enhanced logging and validation.
        """
        book = serializer.save()
        logger.info(
            f"New book created: '{book.title}' by {book.author.name} "
            f"(ID: {book.id}, Year: {book.publication_year})"
        )
        return book
    
    def create(self, request, *args, **kwargs):
        """
        Custom create response with additional information.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = self.perform_create(serializer)
        
        return Response({
            'message': f"Book '{book.title}' created successfully",
            'book': BookSerializer(book).data
        }, status=status.HTTP_201_CREATED)


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book with validation and logging.
    
    Features:
    - PUT/PATCH: Updates book information
    - Requires authentication
    - Maintains data integrity
    - Update logging
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Using the specific permission class
    
    def perform_update(self, serializer):
        """
        Custom update behavior with logging.
        """
        book = serializer.save()
        logger.info(
            f"Book updated: '{book.title}' by {book.author.name} "
            f"(ID: {book.id}, Year: {book.publication_year})"
        )
        return book
    
    def update(self, request, *args, **kwargs):
        """
        Custom update response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        book = self.perform_update(serializer)
        
        return Response({
            'message': f"Book '{book.title}' updated successfully",
            'book': BookSerializer(book).data
        })


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book with confirmation and logging.
    
    Features:
    - DELETE: Removes book from database
    - Requires authentication
    - Deletion logging
    - Confirmation response
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Using the specific permission class
    
    def perform_destroy(self, instance):
        """
        Custom deletion behavior with logging.
        """
        book_title = instance.title
        book_id = instance.id
        author_name = instance.author.name
        
        instance.delete()
        logger.warning(
            f"Book deleted: '{book_title}' by {author_name} (ID: {book_id})"
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy response with confirmation.
        """
        instance = self.get_object()
        book_title = instance.title
        
        self.perform_destroy(instance)
        
        return Response({
            'message': f"Book '{book_title}' deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# CUSTOM API VIEWS - Advanced Functionality
# =============================================================================

class BooksByAuthorView(generics.ListAPIView):
    """
    Custom view to get all books by a specific author.
    
    URL: /books/by-author/<int:author_id>/
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """
        Filter books by author ID from URL parameter.
        """
        author_id = self.kwargs.get('author_id')
        return Book.objects.filter(author_id=author_id).select_related('author')
    
    def list(self, request, *args, **kwargs):
        """
        Custom response with author information.
        """
        author_id = self.kwargs.get('author_id')
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({
                'error': f'Author with ID {author_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        response = super().list(request, *args, **kwargs)
        return Response({
            'message': f"Books by {author.name}",
            'author': AuthorSerializer(author).data,
            'books_count': len(response.data),
            'books': response.data
        })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_statistics(request):
    """
    Custom function-based view for book statistics.
    
    Returns:
    - Total number of books
    - Total number of authors
    - Books per decade
    - Most prolific authors
    """
    from django.db.models import Count
    from collections import defaultdict
    
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    
    # Books per decade
    books_by_decade = defaultdict(int)
    for book in Book.objects.all():
        decade = (book.publication_year // 10) * 10
        books_by_decade[f"{decade}s"] += 1
    
    # Most prolific authors (top 5)
    prolific_authors = Author.objects.annotate(
        book_count=Count('books')
    ).order_by('-book_count')[:5]
    
    return Response({
        'message': 'Book statistics retrieved successfully',
        'statistics': {
            'total_books': total_books,
            'total_authors': total_authors,
            'books_per_decade': dict(books_by_decade),
            'most_prolific_authors': [
                {
                    'name': author.name,
                    'book_count': author.book_count
                }
                for author in prolific_authors
            ]
        }
    })
