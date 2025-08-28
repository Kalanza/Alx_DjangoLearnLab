"""
API endpoint tests using Django's test framework.

This module contains tests to verify that our API endpoints work correctly
and that serializers handle validation as expected.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book
from datetime import date


class ModelTestCase(TestCase):
    """Test cases for Author and Book models."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        
    def test_author_creation(self):
        """Test author model creation."""
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(str(self.author), "Test Author")
        
    def test_book_creation(self):
        """Test book model creation."""
        book = Book.objects.create(
            title="Test Book",
            publication_year=2000,
            author=self.author
        )
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.publication_year, 2000)
        self.assertEqual(book.author, self.author)
        self.assertEqual(str(book), "Test Book (2000)")


class SerializerTestCase(APITestCase):
    """Test cases for custom serializers."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2000,
            author=self.author
        )
        
    def test_author_serializer_with_books(self):
        """Test AuthorSerializer includes nested books."""
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Author")
        self.assertEqual(len(response.data['books']), 1)
        self.assertEqual(response.data['books'][0]['title'], "Test Book")
        
    def test_book_validation_future_year(self):
        """Test that books cannot have future publication years."""
        url = reverse('book-list-create')
        future_year = date.today().year + 1
        
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        
    def test_book_validation_valid_year(self):
        """Test that books with valid years are accepted."""
        url = reverse('book-list-create')
        
        data = {
            'title': 'Valid Book',
            'publication_year': 2020,
            'author': self.author.pk
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Valid Book')


class APIEndpointTestCase(APITestCase):
    """Test cases for API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="API Test Author")
        
    def test_author_list_endpoint(self):
        """Test author list endpoint."""
        url = reverse('author-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_author_create_endpoint(self):
        """Test author creation endpoint."""
        url = reverse('author-list-create')
        data = {'name': 'New Author'}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Author')
        
    def test_book_list_endpoint(self):
        """Test book list endpoint."""
        Book.objects.create(
            title="API Test Book",
            publication_year=2021,
            author=self.author
        )
        
        url = reverse('book-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
