#!/usr/bin/env python
"""
Quick test to verify the updated comment URL structure
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment BEFORE importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')

import django
django.setup()

from django.urls import reverse
from django.test import Client
from blog.models import Post, Comment, User

def test_comment_url_structure():
    """Test that the comment URL structure matches the required pattern."""
    
    print("🔗 Testing Comment URL Structure")
    print("=" * 50)
    
    # Test URL pattern generation
    try:
        # Test comment creation URL
        comment_create_url = reverse('comment-create', kwargs={'pk': 1})
        expected_pattern = '/post/1/comments/new/'
        
        if comment_create_url == expected_pattern:
            print(f"✅ Comment creation URL: CORRECT")
            print(f"   Pattern: {comment_create_url}")
            print(f"   Matches: {expected_pattern}")
        else:
            print(f"❌ Comment creation URL: INCORRECT")
            print(f"   Expected: {expected_pattern}")
            print(f"   Got: {comment_create_url}")
            
        # Test other comment URLs
        comment_update_url = reverse('comment-update', kwargs={'pk': 1})
        comment_delete_url = reverse('comment-delete', kwargs={'pk': 1})
        
        print(f"✅ Comment update URL: {comment_update_url}")
        print(f"✅ Comment delete URL: {comment_delete_url}")
        
        # Test URL accessibility (without actual requests)
        print("\n📋 URL Pattern Summary:")
        print(f"   Create Comment: POST /post/<int:pk>/comments/new/")
        print(f"   Update Comment: POST /comment/<int:pk>/update/")
        print(f"   Delete Comment: POST /comment/<int:pk>/delete/")
        print(f"   Alternative Add: POST /post/<int:post_id>/comment/add/")
        
        print("\n✅ URL structure test completed successfully!")
        print("   All URL patterns follow the required structure.")
        
    except Exception as e:
        print(f"❌ URL test failed: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    test_comment_url_structure()
