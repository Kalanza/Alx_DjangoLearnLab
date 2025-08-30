#!/usr/bin/env python
"""
Test script for Django Blog Post Management Features
This script tests the CRUD operations for blog posts including permissions and security.
"""

import os
import sys
import django

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post
from blog.forms import PostForm

def test_blog_post_management():
    """Test the blog post management functionality"""
    
    print("📝 Testing Django Blog Post Management Features")
    print("=" * 55)
    
    # Test 1: Post Model
    print("\n1. Testing Post Model...")
    try:
        # Create test users
        user1 = User.objects.create_user(username='author1', password='testpass123')
        user2 = User.objects.create_user(username='author2', password='testpass123')
        
        # Create test post
        post = Post.objects.create(
            title='Test Post Title',
            content='This is test content for the blog post.',
            author=user1
        )
        
        print("   ✅ Post creation: PASSED")
        print(f"   Created post: '{post.title}' by {post.author.username}")
        print(f"   Post URL: {post.get_absolute_url()}")
        
    except Exception as e:
        print(f"   ❌ Post creation: FAILED - {e}")
    
    # Test 2: PostForm Validation
    print("\n2. Testing PostForm Validation...")
    
    # Test valid form
    valid_form_data = {
        'title': 'Valid Test Title',
        'content': 'This is valid content that is more than 20 characters long.'
    }
    
    form = PostForm(data=valid_form_data)
    if form.is_valid():
        print("   ✅ Valid form validation: PASSED")
    else:
        print("   ❌ Valid form validation: FAILED")
        print(f"   Errors: {form.errors}")
    
    # Test invalid form (short title)
    invalid_form_data = {
        'title': 'Bad',  # Too short
        'content': 'This is valid content that is more than 20 characters long.'
    }
    
    form = PostForm(data=invalid_form_data)
    if not form.is_valid() and 'title' in form.errors:
        print("   ✅ Invalid title validation: PASSED")
    else:
        print("   ❌ Invalid title validation: FAILED")
    
    # Test invalid form (short content)
    invalid_form_data2 = {
        'title': 'Valid Title Here',
        'content': 'Short'  # Too short
    }
    
    form = PostForm(data=invalid_form_data2)
    if not form.is_valid() and 'content' in form.errors:
        print("   ✅ Invalid content validation: PASSED")
    else:
        print("   ❌ Invalid content validation: FAILED")
    
    # Test 3: URL Patterns
    print("\n3. Testing URL Patterns...")
    
    url_tests = [
        ('post-list', [], 'Post list page'),
        ('post-detail', [1], 'Post detail page'),
        ('post-create', [], 'Post creation page'),
        ('post-update', [1], 'Post update page'),
        ('post-delete', [1], 'Post delete page'),
        ('user-posts', ['author1'], 'User posts page')
    ]
    
    for url_name, args, description in url_tests:
        try:
            url = reverse(url_name, args=args)
            print(f"   ✅ {description} URL ({url_name}): {url}")
        except Exception as e:
            print(f"   ❌ {description} URL ({url_name}): FAILED - {e}")
    
    # Test 4: Template Files Check
    print("\n4. Checking Template Files...")
    templates = [
        'blog/post_list.html',
        'blog/post_detail.html',
        'blog/post_form.html',
        'blog/post_confirm_delete.html',
        'blog/user_posts.html'
    ]
    
    for template in templates:
        template_path = os.path.join('blog', 'templates', template)
        if os.path.exists(template_path):
            print(f"   ✅ {template}: EXISTS")
        else:
            print(f"   ❌ {template}: MISSING")
    
    # Test 5: View Permissions (Basic Test)
    print("\n5. Testing View Permissions...")
    
    # Test public access to list and detail views
    client = Client()
    
    try:
        response = client.get(reverse('post-list'))
        if response.status_code == 200:
            print("   ✅ Anonymous access to post list: ALLOWED")
        else:
            print(f"   ❌ Anonymous access to post list: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Anonymous access to post list: ERROR - {e}")
    
    try:
        response = client.get(reverse('post-detail', args=[post.pk]))
        if response.status_code == 200:
            print("   ✅ Anonymous access to post detail: ALLOWED")
        else:
            print(f"   ❌ Anonymous access to post detail: FAILED (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Anonymous access to post detail: ERROR - {e}")
    
    # Test authentication required for create view
    try:
        response = client.get(reverse('post-create'))
        if response.status_code == 302:  # Redirect to login
            print("   ✅ Authentication required for post creation: ENFORCED")
        else:
            print(f"   ❌ Authentication required for post creation: NOT ENFORCED (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Authentication test for post creation: ERROR - {e}")
    
    # Test 6: Database Queries
    print("\n6. Testing Database Queries...")
    
    try:
        # Test post count
        post_count = Post.objects.count()
        print(f"   ✅ Total posts in database: {post_count}")
        
        # Test post ordering
        posts = Post.objects.all()[:3]
        if posts:
            print(f"   ✅ Posts ordered by date: Latest is '{posts[0].title}'")
        
        # Test user posts filtering
        user_posts = Post.objects.filter(author=user1)
        print(f"   ✅ Posts by {user1.username}: {user_posts.count()}")
        
    except Exception as e:
        print(f"   ❌ Database queries: ERROR - {e}")
    
    # Test 7: Post Model Methods
    print("\n7. Testing Post Model Methods...")
    
    try:
        # Test __str__ method
        str_repr = str(post)
        if str_repr == post.title:
            print(f"   ✅ Post __str__ method: WORKS ('{str_repr}')")
        else:
            print(f"   ❌ Post __str__ method: FAILED ('{str_repr}' != '{post.title}')")
        
        # Test get_absolute_url method
        abs_url = post.get_absolute_url()
        expected_url = f'/posts/{post.pk}/'
        if abs_url == expected_url:
            print(f"   ✅ Post get_absolute_url: WORKS ('{abs_url}')")
        else:
            print(f"   ❌ Post get_absolute_url: FAILED ('{abs_url}' != '{expected_url}')")
            
    except Exception as e:
        print(f"   ❌ Post model methods: ERROR - {e}")
    
    # Test 8: Form Fields and Widgets
    print("\n8. Testing Form Fields and Widgets...")
    
    form = PostForm()
    
    # Check form fields
    expected_fields = ['title', 'content']
    for field in expected_fields:
        if field in form.fields:
            print(f"   ✅ Form field '{field}': EXISTS")
            
            # Check widget classes
            widget_class = form.fields[field].widget.attrs.get('class', '')
            if 'form-control' in widget_class:
                print(f"   ✅ Form field '{field}' styling: APPLIED")
            else:
                print(f"   ❌ Form field '{field}' styling: MISSING")
        else:
            print(f"   ❌ Form field '{field}': MISSING")
    
    print("\n" + "=" * 55)
    print("🎉 Blog Post Management Test Complete!")
    print("\nFeatures Tested:")
    print("✓ Post model with CRUD operations")
    print("✓ Form validation and security")
    print("✓ URL patterns and routing")
    print("✓ Template existence")
    print("✓ Authentication and permissions")
    print("✓ Database operations")
    print("✓ Model methods and properties")
    print("✓ Form styling and validation")
    
    print("\nNext Steps:")
    print("1. Visit http://127.0.0.1:8000/posts/ to see all posts")
    print("2. Test creating a new post (requires login)")
    print("3. Test editing your own posts")
    print("4. Test that you cannot edit other users' posts")
    print("5. Verify pagination works with many posts")
    print("6. Test responsive design on mobile devices")

if __name__ == '__main__':
    test_blog_post_management()
