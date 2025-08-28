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
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
import logging

# Set up logging
logger = logging.getLogger(__name__)


# =============================================================================
# AUTHOR VIEWS - Combined Generic Views
# =============================================================================

class AuthorListCreateView(generics.ListCreateAPIView):
    """
    Combined view for listing all authors and creating new authors.
    
    Features:
    - GET: Returns paginated list of all authors with their nested books
    - POST: Creates a new author with validation
    - Search functionality by author name
    - Ordering by name (ascending/descending)
    - Permission: Read access for all, create requires authentication
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']  # Default ordering
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions for this view.
        GET requests: Allow any user
        POST requests: Require authentication
        """
        if self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
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
        Custom list method with additional response information.
        """
        response = super().list(request, *args, **kwargs)
        response.data = {
            'message': 'Authors retrieved successfully',
            'count': len(response.data),
            'authors': response.data
        }
        return response


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Individual author operations - retrieve, update, and delete.
    
    Features:
    - GET: Returns specific author with nested books
    - PUT/PATCH: Updates author information
    - DELETE: Removes author and cascades to books
    - Permission: Read access for all, modify/delete requires authentication
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """
        Custom permissions based on HTTP method.
        """
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
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
    List all books with advanced filtering and search capabilities.
    
    Features:
    - GET: Returns paginated list of all books
    - Advanced filtering by author, publication year, title
    - Search functionality across title and author name
    - Ordering by multiple fields
    - Permission: Open access for reading
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']
    
    def get_queryset(self):
        """
        Custom queryset with additional filtering options.
        """
        queryset = super().get_queryset()
        
        # Custom filter: books published after a certain year
        year_after = self.request.query_params.get('year_after', None)
        if year_after:
            try:
                queryset = queryset.filter(publication_year__gt=int(year_after))
            except ValueError:
                pass  # Ignore invalid year format
        
        # Custom filter: books published before a certain year
        year_before = self.request.query_params.get('year_before', None)
        if year_before:
            try:
                queryset = queryset.filter(publication_year__lt=int(year_before))
            except ValueError:
                pass
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Custom list response with metadata.
        """
        response = super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        
        response.data = {
            'message': 'Books retrieved successfully',
            'total_count': queryset.count(),
            'filters_applied': {
                'search': request.query_params.get('search', None),
                'author': request.query_params.get('author', None),
                'year_after': request.query_params.get('year_after', None),
                'year_before': request.query_params.get('year_before', None),
            },
            'books': response.data
        }
        return response


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
    permission_classes = [permissions.IsAuthenticated]
    
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
    permission_classes = [permissions.IsAuthenticated]
    
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
    permission_classes = [permissions.IsAuthenticated]
    
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
