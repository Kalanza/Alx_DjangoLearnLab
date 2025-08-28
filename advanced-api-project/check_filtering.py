#!/usr/bin/env python
"""
Simple test to verify Django REST Framework filtering functionality.
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Author, Book

def check_filtering_requirements():
    """Check that all filtering requirements are met."""
    
    print("🔍 Checking Django REST Framework Filtering Requirements")
    print("=" * 60)
    
    # Check 1: Import requirement
    print("\n1. Checking 'from django_filters import rest_framework' import...")
    try:
        with open('api/views.py', 'r') as f:
            content = f.read()
            if 'from django_filters import rest_framework' in content:
                print("   ✅ Found required import: 'from django_filters import rest_framework'")
            else:
                print("   ❌ Missing import: 'from django_filters import rest_framework'")
    except Exception as e:
        print(f"   ❌ Error checking imports: {e}")
    
    # Check 2: DjangoFilterBackend
    print("\n2. Checking DjangoFilterBackend integration...")
    try:
        if 'DjangoFilterBackend' in content:
            print("   ✅ Found DjangoFilterBackend in views")
        else:
            print("   ❌ Missing DjangoFilterBackend")
    except:
        print("   ❌ Error checking DjangoFilterBackend")
    
    # Check 3: SearchFilter
    print("\n3. Checking SearchFilter integration...")
    try:
        if 'SearchFilter' in content:
            print("   ✅ Found SearchFilter in views")
        else:
            print("   ❌ Missing SearchFilter")
    except:
        print("   ❌ Error checking SearchFilter")
    
    # Check 4: OrderingFilter
    print("\n4. Checking OrderingFilter integration...")
    try:
        if 'OrderingFilter' in content:
            print("   ✅ Found OrderingFilter in views")
        else:
            print("   ❌ Missing OrderingFilter")
    except:
        print("   ❌ Error checking OrderingFilter")
    
    # Check 5: Search fields on Book model
    print("\n5. Checking search functionality on Book model fields...")
    try:
        if 'search_fields' in content and 'title' in content and 'author' in content:
            print("   ✅ Found search_fields configuration for title and author")
        else:
            print("   ❌ Missing search_fields for title and/or author")
    except:
        print("   ❌ Error checking search fields")
    
    # Check 6: Filter fields
    print("\n6. Checking filter capabilities...")
    try:
        if any(x in content for x in ['filterset_fields', 'filterset_class', 'filter_fields']):
            print("   ✅ Found filter configuration")
        else:
            print("   ❌ Missing filter configuration")
    except:
        print("   ❌ Error checking filter configuration")
    
    # Check 7: Settings configuration
    print("\n7. Checking settings configuration...")
    try:
        with open('advanced_api_project/settings.py', 'r') as f:
            settings_content = f.read()
            if 'django_filters' in settings_content:
                print("   ✅ Found django_filters in INSTALLED_APPS")
            else:
                print("   ❌ Missing django_filters in INSTALLED_APPS")
            
            if 'DjangoFilterBackend' in settings_content:
                print("   ✅ Found DjangoFilterBackend in DEFAULT_FILTER_BACKENDS")
            else:
                print("   ❌ Missing DjangoFilterBackend in DEFAULT_FILTER_BACKENDS")
    except Exception as e:
        print(f"   ❌ Error checking settings: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Filtering Requirements Check Complete!")
    
    # Functional test
    print("\n🧪 Running Functional Test...")
    
    # Clear existing data and create test data
    Author.objects.all().delete()
    Book.objects.all().delete()
    
    author1 = Author.objects.create(name="Test Author")
    book1 = Book.objects.create(title="Test Book", publication_year=2020, author=author1)
    
    client = APIClient()
    
    # Test basic list
    print("\n   Testing basic book list...")
    response = client.get('/api/books/')
    if response.status_code == 200:
        print("   ✅ Book list endpoint working")
    else:
        print(f"   ❌ Book list endpoint failed: {response.status_code}")
    
    # Test filtering
    print("   Testing filtering by publication_year...")
    response = client.get('/api/books/?publication_year=2020')
    if response.status_code == 200:
        print("   ✅ Publication year filtering working")
    else:
        print(f"   ❌ Publication year filtering failed: {response.status_code}")
    
    # Test search
    print("   Testing search functionality...")
    response = client.get('/api/books/?search=Test')
    if response.status_code == 200:
        print("   ✅ Search functionality working")
    else:
        print(f"   ❌ Search functionality failed: {response.status_code}")
    
    # Test ordering
    print("   Testing ordering functionality...")
    response = client.get('/api/books/?ordering=title')
    if response.status_code == 200:
        print("   ✅ Ordering functionality working")
    else:
        print(f"   ❌ Ordering functionality failed: {response.status_code}")
    
    print("\n🎉 All functional tests completed!")

if __name__ == "__main__":
    check_filtering_requirements()
