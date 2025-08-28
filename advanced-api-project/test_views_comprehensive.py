"""
Comprehensive test script for Django REST Framework Views.

This script tests all the custom and generic views implemented in the API,
including CRUD operations, permissions, filtering, and custom endpoints.
"""

import requests
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Author, Book
from datetime import date


def test_views_manually():
    """
    Manual testing script using Django shell.
    Run this with: python manage.py shell -c "exec(open('test_views_comprehensive.py').read())"
    """
    print("=== Comprehensive View Testing ===")
    
    # Clean up existing data for consistent testing
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Create test data
    print("\n1. Creating test data...")
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Isaac Asimov")
    
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=author1)
    book3 = Book.objects.create(title="1984", publication_year=1949, author=author2)
    book4 = Book.objects.create(title="Animal Farm", publication_year=1945, author=author2)
    book5 = Book.objects.create(title="Foundation", publication_year=1951, author=author3)
    
    print(f"Created {Author.objects.count()} authors and {Book.objects.count()} books")
    
    # Test serializers with the new views context
    print("\n2. Testing Author serialization with nested books...")
    from api.serializers import AuthorSerializer
    author_data = AuthorSerializer(author1).data
    print(f"Author data: {author_data}")
    print(f"Number of books for {author1.name}: {len(author_data['books'])}")
    
    # Test book statistics calculation
    print("\n3. Testing book statistics...")
    from django.db.models import Count
    from collections import defaultdict
    
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    
    # Books per decade
    books_by_decade = defaultdict(int)
    for book in Book.objects.all():
        decade = (book.publication_year // 10) * 10
        books_by_decade[f"{decade}s"] += 1
    
    # Most prolific authors
    prolific_authors = Author.objects.annotate(
        book_count=Count('books')
    ).order_by('-book_count')[:3]
    
    print(f"Total books: {total_books}")
    print(f"Total authors: {total_authors}")
    print(f"Books per decade: {dict(books_by_decade)}")
    print("Most prolific authors:")
    for author in prolific_authors:
        print(f"  - {author.name}: {author.book_count} books")
    
    # Test filtering functionality
    print("\n4. Testing filtering functionality...")
    
    # Books after 1950
    books_after_1950 = Book.objects.filter(publication_year__gt=1950)
    print(f"Books published after 1950: {books_after_1950.count()}")
    for book in books_after_1950:
        print(f"  - {book.title} ({book.publication_year})")
    
    # Books by specific author
    rowling_books = Book.objects.filter(author=author1)
    print(f"\nBooks by {author1.name}: {rowling_books.count()}")
    for book in rowling_books:
        print(f"  - {book.title} ({book.publication_year})")
    
    print("\n=== Manual testing completed successfully! ===")


class ViewPermissionTestCase(APITestCase):
    """
    Test cases for view permissions and authentication.
    """
    
    def setUp(self):
        """Set up test data and authenticated user."""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", 
            publication_year=2020, 
            author=self.author
        )
    
    def test_author_list_anonymous_access(self):
        """Test that anonymous users can read author list."""
        url = reverse('author-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('authors', response.data)
    
    def test_author_create_requires_authentication(self):
        """Test that creating authors requires authentication."""
        url = reverse('author-list-create')
        data = {'name': 'New Author'}
        
        # Test without authentication
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_book_list_anonymous_access(self):
        """Test that anonymous users can read book list."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('books', response.data)
    
    def test_book_create_requires_authentication(self):
        """Test that creating books requires authentication."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        
        # Test without authentication
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
    
    def test_book_update_requires_authentication(self):
        """Test that updating books requires authentication."""
        url = reverse('book-update', kwargs={'pk': self.book.pk})
        data = {'title': 'Updated Book Title'}
        
        # Test without authentication
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
    
    def test_book_delete_requires_authentication(self):
        """Test that deleting books requires authentication."""
        url = reverse('book-delete', kwargs={'pk': self.book.pk})
        
        # Test without authentication
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ViewFilteringTestCase(APITestCase):
    """
    Test cases for view filtering and search functionality.
    """
    
    def setUp(self):
        """Set up test data."""
        self.author1 = Author.objects.create(name="Fantasy Author")
        self.author2 = Author.objects.create(name="Sci-Fi Author")
        
        self.book1 = Book.objects.create(title="Magic Book", publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title="Space Adventure", publication_year=2010, author=self.author2)
        self.book3 = Book.objects.create(title="Dragon Tale", publication_year=1995, author=self.author1)
    
    def test_book_list_search(self):
        """Test search functionality in book list."""
        url = reverse('book-list')
        
        # Search by title
        response = self.client.get(url, {'search': 'Magic'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Magic Book')
    
    def test_book_list_filter_by_author(self):
        """Test filtering by author."""
        url = reverse('book-list')
        
        response = self.client.get(url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 2)  # author1 has 2 books
    
    def test_book_list_custom_year_filters(self):
        """Test custom year filtering."""
        url = reverse('book-list')
        
        # Books after 1999
        response = self.client.get(url, {'year_after': 1999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 2)  # 2000 and 2010
        
        # Books before 2005
        response = self.client.get(url, {'year_before': 2005})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['books']), 2)  # 1995 and 2000
    
    def test_books_by_author_view(self):
        """Test the custom books by author view."""
        url = reverse('books-by-author', kwargs={'author_id': self.author1.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('author', response.data)
        self.assertIn('books', response.data)
        self.assertEqual(len(response.data['books']), 2)
        self.assertEqual(response.data['author']['name'], 'Fantasy Author')
    
    def test_book_statistics_view(self):
        """Test the book statistics view."""
        url = reverse('book-statistics')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('statistics', response.data)
        
        stats = response.data['statistics']
        self.assertIn('total_books', stats)
        self.assertIn('total_authors', stats)
        self.assertIn('books_per_decade', stats)
        self.assertIn('most_prolific_authors', stats)
        
        self.assertEqual(stats['total_books'], 3)
        self.assertEqual(stats['total_authors'], 2)


class CustomResponseTestCase(APITestCase):
    """
    Test cases for custom response formatting.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.author = Author.objects.create(name="Response Test Author")
        self.book = Book.objects.create(
            title="Response Test Book", 
            publication_year=2021, 
            author=self.author
        )
    
    def test_book_detail_includes_related_books(self):
        """Test that book detail view includes related books by same author."""
        # Create another book by the same author
        Book.objects.create(title="Another Book", publication_year=2022, author=self.author)
        
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('book', response.data)
        self.assertIn('related_books_by_author', response.data)
        self.assertEqual(len(response.data['related_books_by_author']), 1)
    
    def test_custom_create_response(self):
        """Test custom response format for book creation."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'Custom Response Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('book', response.data)
        self.assertIn('Custom Response Book', response.data['message'])
    
    def test_custom_update_response(self):
        """Test custom response format for book update."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book.pk})
        data = {'title': 'Updated Title'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('book', response.data)
        self.assertIn('Updated Title', response.data['message'])


# Run manual tests when executed directly
if __name__ == "__main__":
    test_views_manually()
