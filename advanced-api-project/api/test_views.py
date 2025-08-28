"""
Comprehensive Unit Tests for Django REST Framework APIs

This module contains comprehensive unit tests for the API endpoints,
covering CRUD operations, filtering, searching, ordering, permissions,
and authentication scenarios.

Test Coverage:
- Book model CRUD operations
- Author model CRUD operations  
- Filtering functionality
- Searching functionality
- Ordering functionality
- Permission and authentication scenarios
- Data integrity and validation
- Error handling and edge cases
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date
from .models import Author, Book
import json


class BookCRUDTestCase(APITestCase):
    """Test CRUD operations for Book model endpoints."""
    
    def setUp(self):
        """Set up test data for each test."""
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        
        # Create test books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_book_list_get_success(self):
        """Test successful retrieval of book list."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response structure
        if 'results' in response.data:
            # Paginated response
            data = response.data['results']
            self.assertIn('books', data)
            self.assertGreaterEqual(len(data['books']), 2)
            book_titles = [book['title'] for book in data['books']]
        else:
            # Non-paginated response
            self.assertIn('books', response.data)
            self.assertGreaterEqual(len(response.data['books']), 2)
            book_titles = [book['title'] for book in response.data['books']]
        
        # Check that book data is correctly returned
        self.assertIn("Harry Potter and the Philosopher's Stone", book_titles)
        self.assertIn("1984", book_titles)
    
    def test_book_create_authenticated_success(self):
        """Test successful book creation with authentication."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-create')
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('book', response.data)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        
        # Verify book was actually created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
    
    def test_book_create_unauthenticated_failure(self):
        """Test book creation fails without authentication."""
        url = reverse('book-create')
        
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify book was not created
        self.assertFalse(Book.objects.filter(title='Unauthorized Book').exists())
    
    def test_book_create_invalid_data_failure(self):
        """Test book creation with invalid data."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-create')
        
        # Test with future publication year
        future_year = date.today().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_book_detail_get_success(self):
        """Test successful retrieval of book detail."""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle different response structures
        if 'book' in response.data:
            # Wrapped response
            book_data = response.data['book']
        else:
            # Direct response
            book_data = response.data
            
        self.assertEqual(book_data['title'], self.book1.title)
        self.assertEqual(book_data['publication_year'], self.book1.publication_year)
        self.assertEqual(book_data['author'], self.book1.author.pk)
    
    def test_book_detail_not_found(self):
        """Test book detail with non-existent ID."""
        url = reverse('book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_book_update_authenticated_success(self):
        """Test successful book update with authentication."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        
        data = {
            'title': 'Updated Book Title',
            'publication_year': 1998,
            'author': self.author1.pk
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify book was actually updated in database
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Updated Book Title')
        self.assertEqual(updated_book.publication_year, 1998)
    
    def test_book_update_unauthenticated_failure(self):
        """Test book update fails without authentication."""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 2000,
            'author': self.author1.pk
        }
        
        response = self.client.put(url, data, format='json')
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify book was not updated
        book = Book.objects.get(pk=self.book1.pk)
        self.assertNotEqual(book.title, 'Unauthorized Update')
    
    def test_book_partial_update_success(self):
        """Test successful partial book update (PATCH)."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        
        data = {'title': 'Partially Updated Title'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only title was updated
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertEqual(updated_book.title, 'Partially Updated Title')
        self.assertEqual(updated_book.publication_year, 1997)  # Should remain unchanged
    
    def test_book_delete_authenticated_success(self):
        """Test successful book deletion with authentication."""
        self.client.force_authenticate(user=self.regular_user)
        
        # Create a book specifically for deletion
        book_to_delete = Book.objects.create(
            title='Book to Delete',
            publication_year=2000,
            author=self.author1
        )
        
        url = reverse('book-delete', kwargs={'pk': book_to_delete.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was actually deleted
        self.assertFalse(Book.objects.filter(pk=book_to_delete.pk).exists())
    
    def test_book_delete_unauthenticated_failure(self):
        """Test book deletion fails without authentication."""
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify book was not deleted
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())


class AuthorCRUDTestCase(APITestCase):
    """Test CRUD operations for Author model endpoints."""
    
    def setUp(self):
        """Set up test data for each test."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")
        
        # Create some books for authors
        Book.objects.create(
            title="Book by Author 1",
            publication_year=2020,
            author=self.author1
        )
        
        self.client = APIClient()
    
    def test_author_list_get_success(self):
        """Test successful retrieval of author list."""
        url = reverse('author-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response structure
        if 'results' in response.data:
            # Paginated response
            data = response.data['results']
            self.assertIn('authors', data)
            self.assertGreaterEqual(len(data['authors']), 2)
        else:
            # Non-paginated response
            self.assertIn('authors', response.data)
            self.assertGreaterEqual(len(response.data['authors']), 2)
    
    def test_author_create_authenticated_success(self):
        """Test successful author creation with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('author-list-create')
        
        data = {'name': 'New Test Author'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Test Author')
        
        # Verify author was actually created
        self.assertTrue(Author.objects.filter(name='New Test Author').exists())
    
    def test_author_create_unauthenticated_failure(self):
        """Test author creation fails without authentication."""
        url = reverse('author-list-create')
        
        data = {'name': 'Unauthorized Author'}
        
        response = self.client.post(url, data, format='json')
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify author was not created
        self.assertFalse(Author.objects.filter(name='Unauthorized Author').exists())
    
    def test_author_detail_get_success(self):
        """Test successful retrieval of author detail with nested books."""
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
        self.assertIn('books', response.data)
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], 'Book by Author 1')
    
    def test_author_update_success(self):
        """Test successful author update."""
        self.client.force_authenticate(user=self.user)
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        
        data = {'name': 'Updated Author Name'}
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Author Name')
        
        # Verify author was actually updated
        updated_author = Author.objects.get(pk=self.author1.pk)
        self.assertEqual(updated_author.name, 'Updated Author Name')
    
    def test_author_delete_success(self):
        """Test successful author deletion."""
        self.client.force_authenticate(user=self.user)
        
        # Create an author specifically for deletion (without books)
        author_to_delete = Author.objects.create(name='Author to Delete')
        
        url = reverse('author-detail', kwargs={'pk': author_to_delete.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify author was actually deleted
        self.assertFalse(Author.objects.filter(pk=author_to_delete.pk).exists())


class FilteringSearchingOrderingTestCase(APITestCase):
    """Test filtering, searching, and ordering functionality."""
    
    def setUp(self):
        """Set up test data for filtering and searching tests."""
        # Create authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        self.author3 = Author.objects.create(name="Jane Austen")
        
        # Create books with different years and authors
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author2
        )
        self.book5 = Book.objects.create(
            title="Pride and Prejudice",
            publication_year=1813,
            author=self.author3
        )
        
        self.client = APIClient()
    
    def _extract_books_from_response(self, response):
        """Helper method to extract books from potentially paginated response."""
        if 'results' in response.data:
            # Paginated response
            return response.data['results']['books']
        else:
            # Non-paginated response
            return response.data['books']
    
    def _extract_authors_from_response(self, response):
        """Helper method to extract authors from potentially paginated response."""
        if 'results' in response.data:
            # Paginated response
            return response.data['results']['authors']
        else:
            # Non-paginated response
            return response.data['authors']
    
    def test_book_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        
        # Should return only books from 1997
        for book in books:
            self.assertEqual(book['publication_year'], 1997)
    
    def test_book_filter_by_author(self):
        """Test filtering books by author ID."""
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        for book in books:
            self.assertEqual(book['author'], self.author1.pk)
    
    def test_book_search_by_title(self):
        """Test searching books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        # Should return Harry Potter books
        self.assertGreaterEqual(len(books), 2)
        for book in books:
            self.assertIn('Harry', book['title'])
    
    def test_book_search_by_author_name(self):
        """Test searching books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        # Should return books by George Orwell
        expected_titles = ['1984', 'Animal Farm']
        book_titles = [book['title'] for book in books]
        
        for title in expected_titles:
            self.assertIn(title, book_titles)
    
    def test_book_ordering_by_title_ascending(self):
        """Test ordering books by title (ascending)."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        titles = [book['title'] for book in books]
        
        # Verify titles are in ascending order
        self.assertEqual(titles, sorted(titles))
    
    def test_book_ordering_by_publication_year_descending(self):
        """Test ordering books by publication year (descending)."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        years = [book['publication_year'] for book in books]
        
        # Verify years are in descending order
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_author_search_functionality(self):
        """Test author search functionality."""
        url = reverse('author-list-create')
        response = self.client.get(url, {'search': 'J.K.'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        authors = self._extract_authors_from_response(response)
        # Should return J.K. Rowling
        self.assertGreaterEqual(len(authors), 1)
        
        found_jk = False
        for author in authors:
            if 'J.K.' in author['name']:
                found_jk = True
                break
        self.assertTrue(found_jk)
    
    def test_combined_filtering_and_ordering(self):
        """Test combined filtering and ordering."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'author_name': 'Rowling',
            'ordering': 'publication_year'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        
        # Should return only Rowling's books
        self.assertGreaterEqual(len(books), 2)
        
        # Should be ordered by publication year
        years = [book['publication_year'] for book in books]
        self.assertEqual(years, sorted(years))
    
    def test_advanced_filtering_by_decade(self):
        """Test advanced filtering by decade."""
        url = reverse('book-list')
        response = self.client.get(url, {'decade': '1990s'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        books = self._extract_books_from_response(response)
        # Should return books from 1990s
        for book in books:
            year = book['publication_year']
            self.assertTrue(1990 <= year <= 1999)


class PermissionAndAuthenticationTestCase(APITestCase):
    """Test permission and authentication scenarios."""
    
    def setUp(self):
        """Set up test data for permission tests."""
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='regularpass123'
        )
        
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        
        self.client = APIClient()
    
    def test_book_list_anonymous_access(self):
        """Test that anonymous users can read book list."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_detail_anonymous_access(self):
        """Test that anonymous users can read book details."""
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_create_requires_authentication(self):
        """Test that book creation requires authentication."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_update_requires_authentication(self):
        """Test that book update requires authentication."""
        url = reverse('book-update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Updated Book',
            'publication_year': 2021,
            'author': self.author.pk
        }
        
        response = self.client.put(url, data, format='json')
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_book_delete_requires_authentication(self):
        """Test that book deletion requires authentication."""
        url = reverse('book-delete', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_author_list_anonymous_access(self):
        """Test that anonymous users can read author list."""
        url = reverse('author-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_author_create_requires_authentication(self):
        """Test that author creation requires authentication."""
        url = reverse('author-list-create')
        data = {'name': 'New Author'}
        
        response = self.client.post(url, data, format='json')
        
        # DRF returns 403 Forbidden instead of 401 for permission denied
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_authenticated_user_can_create_book(self):
        """Test that authenticated users can create books."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-create')
        
        data = {
            'title': 'Authenticated Book',
            'publication_year': 2021,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_authenticated_user_can_update_book(self):
        """Test that authenticated users can update books."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-update', kwargs={'pk': self.book.pk})
        
        data = {
            'title': 'Updated by Regular User',
            'publication_year': 2021,
            'author': self.author.pk
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_user_can_delete_book(self):
        """Test that authenticated users can delete books."""
        # Create a book specifically for deletion
        book_to_delete = Book.objects.create(
            title='Book for Deletion',
            publication_year=2020,
            author=self.author
        )
        
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-delete', kwargs={'pk': book_to_delete.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DataIntegrityAndValidationTestCase(APITestCase):
    """Test data integrity and validation scenarios."""
    
    def setUp(self):
        """Set up test data for validation tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_book_creation_with_future_year_fails(self):
        """Test that books cannot be created with future publication years."""
        url = reverse('book-create')
        future_year = date.today().year + 1
        
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_book_creation_with_missing_fields_fails(self):
        """Test that book creation fails with missing required fields."""
        url = reverse('book-create')
        
        # Missing title
        data = {
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_book_creation_with_invalid_author_fails(self):
        """Test that book creation fails with non-existent author."""
        url = reverse('book-create')
        
        data = {
            'title': 'Test Book',
            'publication_year': 2020,
            'author': 99999  # Non-existent author ID
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('author', response.data)
    
    def test_author_creation_with_empty_name_fails(self):
        """Test that author creation fails with empty name."""
        url = reverse('author-list-create')
        
        data = {'name': ''}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
    
    def test_book_update_with_invalid_data_fails(self):
        """Test that book update fails with invalid data."""
        book = Book.objects.create(
            title='Original Book',
            publication_year=2020,
            author=self.author
        )
        
        url = reverse('book-update', kwargs={'pk': book.pk})
        future_year = date.today().year + 1
        
        data = {
            'title': '',  # Empty title
            'publication_year': future_year,  # Future year
            'author': 99999  # Non-existent author
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Should have errors for multiple fields
        self.assertIn('title', response.data)
        self.assertIn('publication_year', response.data)
        self.assertIn('author', response.data)


class ErrorHandlingTestCase(APITestCase):
    """Test error handling and edge cases."""
    
    def setUp(self):
        """Set up test data for error handling tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.client = APIClient()
    
    def test_book_detail_with_invalid_id(self):
        """Test book detail with invalid ID returns 404."""
        url = reverse('book-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_book_update_with_invalid_id(self):
        """Test book update with invalid ID returns 404."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': 99999})
        
        data = {
            'title': 'Updated Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_book_delete_with_invalid_id(self):
        """Test book deletion with invalid ID returns 404."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': 99999})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_author_detail_with_invalid_id(self):
        """Test author detail with invalid ID returns 404."""
        url = reverse('author-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_malformed_json_request(self):
        """Test handling of malformed JSON requests."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        
        # Send malformed JSON
        response = self.client.post(
            url,
            data='{"title": "Test Book", "publication_year": }',  # Malformed JSON
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_filtering_parameters(self):
        """Test handling of invalid filtering parameters."""
        url = reverse('book-list')
        
        # Test with invalid year format
        response = self.client.get(url, {'publication_year': 'invalid_year'})
        
        # Should return 400 for invalid filter value or 200 and ignore invalid filter
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
    
    def test_invalid_ordering_parameters(self):
        """Test handling of invalid ordering parameters."""
        url = reverse('book-list')
        
        # Test with invalid ordering field
        response = self.client.get(url, {'ordering': 'invalid_field'})
        
        # Should still return 200 but use default ordering
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ResponseFormatTestCase(APITestCase):
    """Test response format and structure."""
    
    def setUp(self):
        """Set up test data for response format tests."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        self.client = APIClient()
    
    def test_book_list_response_structure(self):
        """Test book list response has correct structure."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response structure
        if 'results' in response.data:
            # Paginated response - check pagination structure
            self.assertIn('count', response.data)
            self.assertIn('results', response.data)
            
            # Check the actual data structure
            data = response.data['results']
            required_fields = ['message', 'total_count', 'books']
            for field in required_fields:
                self.assertIn(field, data)
            
            # Check book structure
            if data['books']:
                book = data['books'][0]
                required_book_fields = ['id', 'title', 'publication_year', 'author']
                for field in required_book_fields:
                    self.assertIn(field, book)
        else:
            # Non-paginated response
            required_fields = ['message', 'total_count', 'books']
            for field in required_fields:
                self.assertIn(field, response.data)
            
            # Check book structure
            if response.data['books']:
                book = response.data['books'][0]
                required_book_fields = ['id', 'title', 'publication_year', 'author']
                for field in required_book_fields:
                    self.assertIn(field, book)
    
    def test_author_list_response_structure(self):
        """Test author list response has correct structure."""
        url = reverse('author-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response structure
        if 'results' in response.data:
            # Paginated response - check pagination structure
            self.assertIn('count', response.data)
            self.assertIn('results', response.data)
            
            # Check the actual data structure
            data = response.data['results']
            required_fields = ['message', 'total_count', 'authors']
            for field in required_fields:
                self.assertIn(field, data)
            
            # Check author structure with nested books
            if data['authors']:
                author = data['authors'][0]
                required_author_fields = ['id', 'name', 'books']
                for field in required_author_fields:
                    self.assertIn(field, author)
        else:
            # Non-paginated response
            required_fields = ['message', 'total_count', 'authors']
            for field in required_fields:
                self.assertIn(field, response.data)
            
            # Check author structure with nested books
            if response.data['authors']:
                author = response.data['authors'][0]
                required_author_fields = ['id', 'name', 'books']
                for field in required_author_fields:
                    self.assertIn(field, author)
    
    def test_book_creation_response_structure(self):
        """Test book creation response has correct structure."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        
        data = {
            'title': 'Response Test Book',
            'publication_year': 2021,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response structure
        required_fields = ['message', 'book']
        for field in required_fields:
            self.assertIn(field, response.data)
        
        # Check created book structure
        book = response.data['book']
        required_book_fields = ['id', 'title', 'publication_year', 'author']
        for field in required_book_fields:
            self.assertIn(field, book)
    
    def test_error_response_structure(self):
        """Test error responses have proper structure."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        
        # Send invalid data to trigger validation error
        data = {
            'title': '',  # Empty title should cause validation error
            'publication_year': 2021,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Error response should contain field-specific errors
        self.assertIn('title', response.data)
        self.assertIsInstance(response.data['title'], list)
