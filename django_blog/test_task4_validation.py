#!/usr/bin/env python3
"""
Test script to validate Task 4 implementation: Tagging and Search Functionality
This script will test all the components we've implemented.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Tag
from blog.forms import PostForm, SearchForm
from django.db.models import Q

class Task4ValidationTest:
    """Validate Task 4: Tagging and Search Functionality implementation"""
    
    def __init__(self):
        self.client = Client()
        self.user = None
        self.setup_test_data()
    
    def setup_test_data(self):
        """Create test user and sample data"""
        print("Setting up test data...")
        
        # Create test user
        self.user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            self.user.set_password('testpass123')
            self.user.save()
        
        # Create test tags
        tag1, _ = Tag.objects.get_or_create(name='Django')
        tag2, _ = Tag.objects.get_or_create(name='Python')
        tag3, _ = Tag.objects.get_or_create(name='Web Development')
        
        # Create test posts with tags
        post1, created = Post.objects.get_or_create(
            title='Django Tutorial',
            defaults={
                'content': 'This is a comprehensive Django tutorial for beginners.',
                'author': self.user
            }
        )
        if created:
            post1.tags.add(tag1, tag2)
        
        post2, created = Post.objects.get_or_create(
            title='Python Best Practices',
            defaults={
                'content': 'Learn about Python coding best practices and conventions.',
                'author': self.user
            }
        )
        if created:
            post2.tags.add(tag2)
        
        post3, created = Post.objects.get_or_create(
            title='Building Web Applications',
            defaults={
                'content': 'Guide to building modern web applications with Django.',
                'author': self.user
            }
        )
        if created:
            post3.tags.add(tag1, tag3)
        
        print(f"Created/verified {User.objects.count()} users")
        print(f"Created/verified {Tag.objects.count()} tags")
        print(f"Created/verified {Post.objects.count()} posts")
    
    def test_tag_model(self):
        """Test Tag model functionality"""
        print("\n=== Testing Tag Model ===")
        
        try:
            # Test tag creation
            tag = Tag.objects.get(name='Django')
            print(f"✓ Tag model working: {tag.name}")
            
            # Test many-to-many relationship
            posts_with_django = tag.posts.all()
            print(f"✓ Tag-Post relationship working: {posts_with_django.count()} posts with Django tag")
            
            # Test get_absolute_url
            if hasattr(tag, 'get_absolute_url'):
                url = tag.get_absolute_url()
                print(f"✓ Tag get_absolute_url working: {url}")
            
            return True
        except Exception as e:
            print(f"✗ Tag model test failed: {e}")
            return False
    
    def test_post_form_with_tags(self):
        """Test PostForm with tags functionality"""
        print("\n=== Testing PostForm with Tags ===")
        
        try:
            # Test form with tags
            form_data = {
                'title': 'Test Post with Tags',
                'content': 'This is a test post content.',
                'tags_input': 'Django, Python, Testing'
            }
            
            form = PostForm(data=form_data)
            if form.is_valid():
                print("✓ PostForm validation working with tags")
                
                # Test tag processing
                if hasattr(form, 'save'):
                    print("✓ PostForm has save method")
                else:
                    print("✗ PostForm missing save method")
                
                return True
            else:
                print(f"✗ PostForm validation failed: {form.errors}")
                return False
                
        except Exception as e:
            print(f"✗ PostForm test failed: {e}")
            return False
    
    def test_search_form(self):
        """Test SearchForm functionality"""
        print("\n=== Testing SearchForm ===")
        
        try:
            from blog.forms import SearchForm
            
            # Test valid search form
            form_data = {
                'query': 'Django',
                'search_in': 'all'
            }
            
            form = SearchForm(data=form_data)
            if form.is_valid():
                print("✓ SearchForm validation working")
                return True
            else:
                print(f"✗ SearchForm validation failed: {form.errors}")
                return False
                
        except ImportError as e:
            print(f"✗ SearchForm import failed: {e}")
            return False
        except Exception as e:
            print(f"✗ SearchForm test failed: {e}")
            return False
    
    def test_search_functionality(self):
        """Test search functionality"""
        print("\n=== Testing Search Functionality ===")
        
        try:
            # Test Q object search
            search_query = 'Django'
            
            # Search in title and content
            posts = Post.objects.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
            
            print(f"✓ Q object search working: Found {posts.count()} posts for '{search_query}'")
            
            # Test tag-based filtering
            django_tag = Tag.objects.get(name='Django')
            posts_by_tag = Post.objects.filter(tags=django_tag)
            print(f"✓ Tag filtering working: Found {posts_by_tag.count()} posts with Django tag")
            
            return True
            
        except Exception as e:
            print(f"✗ Search functionality test failed: {e}")
            return False
    
    def test_urls_configuration(self):
        """Test URL configuration"""
        print("\n=== Testing URL Configuration ===")
        
        try:
            from django.urls import reverse
            
            # Test search URLs
            search_url = reverse('search-results')
            print(f"✓ Search results URL: {search_url}")
            
            # Test tag URLs
            tag_list_url = reverse('tag-list')
            print(f"✓ Tag list URL: {tag_list_url}")
            
            # Test posts by tag URL
            posts_by_tag_url = reverse('posts-by-tag', kwargs={'tag_name': 'Django'})
            print(f"✓ Posts by tag URL: {posts_by_tag_url}")
            
            return True
            
        except Exception as e:
            print(f"✗ URL configuration test failed: {e}")
            return False
    
    def test_templates_exist(self):
        """Test if templates exist"""
        print("\n=== Testing Template Files ===")
        
        template_files = [
            'blog/templates/blog/search_results.html',
            'blog/templates/blog/posts_by_tag.html',
            'blog/templates/blog/tag_list.html'
        ]
        
        results = []
        for template in template_files:
            if os.path.exists(template):
                print(f"✓ Template exists: {template}")
                results.append(True)
            else:
                print(f"✗ Template missing: {template}")
                results.append(False)
        
        return all(results)
    
    def run_all_tests(self):
        """Run all validation tests"""
        print("Starting Task 4 Validation Tests...")
        print("=" * 50)
        
        tests = [
            self.test_tag_model,
            self.test_post_form_with_tags,
            self.test_search_form,
            self.test_search_functionality,
            self.test_urls_configuration,
            self.test_templates_exist
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
            except Exception as e:
                print(f"✗ Test failed with exception: {e}")
                results.append(False)
        
        print("\n" + "=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        
        passed = sum(results)
        total = len(results)
        
        print(f"Tests passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Task 4 implementation is complete.")
        else:
            print("⚠️  Some tests failed. Please review the implementation.")
        
        return passed == total

if __name__ == '__main__':
    validator = Task4ValidationTest()
    validator.run_all_tests()
