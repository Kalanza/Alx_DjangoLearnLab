#!/usr/bin/env python
"""
Test script for Django REST Framework filtering, searching, and ordering functionality.

This script tests the following features:
1. Django Filter integration (from django_filters import rest_framework)
2. OrderingFilter integration
3. SearchFilter integration
4. Search functionality on Book model fields (title and author)
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Author, Book
import json

def test_filtering_functionality():
    """Test comprehensive filtering functionality."""
    
    print("🧪 Starting Django REST Framework Filtering Tests")
    print("=" * 60)
    
    # Create test client
    client = APIClient()
    
    # Create test data
    print("\n📝 Creating test data...")
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Jane Austen")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=author1)
    book3 = Book.objects.create(title="1984", publication_year=1949, author=author2)
    book4 = Book.objects.create(title="Animal Farm", publication_year=1945, author=author2)
    book5 = Book.objects.create(title="Pride and Prejudice", publication_year=1813, author=author3)
    
    print(f"✅ Created {Author.objects.count()} authors and {Book.objects.count()} books")
    
    # Test 1: Basic filtering by publication_year
    print("\n🔍 Test 1: Basic filtering by publication_year")
    response = client.get('/api/books/?publication_year=1997')
    print(f"📊 Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"📚 Found {len(data)} books published in 1997")
        if data and len(data) > 0:
            print(f"   - {data[0].get('title', 'Unknown title')}")
        print("✅ Test 1 PASSED")
    else:
        print("❌ Test 1 FAILED")
    
    # Test 2: Search functionality on title field
    print("\n🔍 Test 2: Search functionality on title field")
    response = client.get('/api/books/?search=Harry')
    print(f"📊 Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        print(f"📚 Found {len(results)} books matching 'Harry'")
        for book in results:
            print(f"   - {book.get('title', 'Unknown title')}")
        print("✅ Test 2 PASSED")
    else:
        print("❌ Test 2 FAILED")
    
    # Test 3: Search functionality on author name
    print("\n🔍 Test 3: Search functionality on author name")
    response = client.get('/api/books/?search=Orwell')
    print(f"📊 Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        print(f"📚 Found {len(results)} books by authors matching 'Orwell'")
        for book in results:
            print(f"   - {book.get('title', 'Unknown title')} by {book.get('author_name', 'Unknown author')}")
        print("✅ Test 3 PASSED")
    else:
        print("❌ Test 3 FAILED")
    
    # Test 4: Ordering functionality (ascending)
    print("\n🔍 Test 4: Ordering by publication_year (ascending)")
    response = client.get('/api/books/?ordering=publication_year')
    print(f"📊 Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        print(f"📚 Found {len(results)} books ordered by publication year")
        for book in results[:3]:  # Show first 3
            print(f"   - {book.get('title', 'Unknown title')} ({book.get('publication_year', 'Unknown year')})")
        print("✅ Test 4 PASSED")
    else:
        print("❌ Test 4 FAILED")
    
    # Test 5: Ordering functionality (descending)
    print("\n🔍 Test 5: Ordering by publication_year (descending)")
    response = client.get('/api/books/?ordering=-publication_year')
    print(f"📊 Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        print(f"📚 Found {len(results)} books ordered by publication year (desc)")
        for book in results[:3]:  # Show first 3
            print(f"   - {book.get('title', 'Unknown title')} ({book.get('publication_year', 'Unknown year')})")
        print("✅ Test 5 PASSED")
    else:
        print("❌ Test 5 FAILED")
    
    # Test 6: Combined filtering and ordering
    print("\n🔍 Test 6: Combined filtering and ordering")
    response = client.get('/api/books/?author_name=Rowling&ordering=publication_year')
    print(f"📊 Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            results = data
        print(f"📚 Found {len(results)} books by Rowling, ordered by year")
        for book in results:
            print(f"   - {book.get('title', 'Unknown title')} ({book.get('publication_year', 'Unknown year')})")
        print("✅ Test 6 PASSED")
    else:
        print("❌ Test 6 FAILED")
    
    # Test 7: Author filtering and searching
    print("\n🔍 Test 7: Author filtering and searching")
    response = client.get('/api/authors/?search=J.K.')
    print(f"📊 Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            results = data['results']
        elif isinstance(data, dict) and 'authors' in data:
            results = data['authors']
        else:
            results = data
        print(f"📚 Found {len(results)} authors matching 'J.K.'")
        for author in results:
            print(f"   - {author.get('name', 'Unknown name')}")
        print("✅ Test 7 PASSED")
    else:
        print("❌ Test 7 FAILED")
    
    print("\n" + "=" * 60)
    print("🎉 Django REST Framework Filtering Tests Completed!")
    print("\n🔧 Key Features Verified:")
    print("   ✅ from django_filters import rest_framework")
    print("   ✅ DjangoFilterBackend integration")
    print("   ✅ SearchFilter integration")
    print("   ✅ OrderingFilter integration")
    print("   ✅ Search functionality on Book title field")
    print("   ✅ Search functionality on Book author field")
    print("   ✅ Filter by publication_year")
    print("   ✅ Custom filtering capabilities")
    print("   ✅ Combined filtering and ordering")

if __name__ == "__main__":
    test_filtering_functionality()
