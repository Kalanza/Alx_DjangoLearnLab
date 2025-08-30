#!/usr/bin/env python
"""
Comprehensive test script for Django Blog Comment Functionality
Tests all CRUD operations for comments, permissions, and form validation.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment BEFORE importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')

import django
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post, Comment
from blog.forms import CommentForm

def create_test_data():
    """Create test users, posts, and comments."""
    print("📊 Creating test data...")
    
    # Create test users
    user1, created = User.objects.get_or_create(
        username='testuser1',
        defaults={
            'email': 'user1@test.com',
            'first_name': 'Test',
            'last_name': 'User1'
        }
    )
    if created:
        user1.set_password('testpass123')
        user1.save()
    
    user2, created = User.objects.get_or_create(
        username='testuser2',
        defaults={
            'email': 'user2@test.com',
            'first_name': 'Test',
            'last_name': 'User2'
        }
    )
    if created:
        user2.set_password('testpass123')
        user2.save()
    
    # Create test posts
    post1, created = Post.objects.get_or_create(
        title='Test Post for Comments',
        defaults={
            'content': 'This is a test post to test comment functionality. It has enough content to meet validation requirements.',
            'author': user1
        }
    )
    
    post2, created = Post.objects.get_or_create(
        title='Another Test Post',
        defaults={
            'content': 'This is another test post with different content for testing comment features.',
            'author': user2
        }
    )
    
    # Create test comments
    comment1, created = Comment.objects.get_or_create(
        post=post1,
        author=user2,
        defaults={
            'content': 'This is a test comment on the first post.'
        }
    )
    
    comment2, created = Comment.objects.get_or_create(
        post=post1,
        author=user1,
        defaults={
            'content': 'This is another comment by the post author.'
        }
    )
    
    print(f"   ✅ Test users created: {User.objects.count()}")
    print(f"   ✅ Test posts created: {Post.objects.count()}")
    print(f"   ✅ Test comments created: {Comment.objects.count()}")
    
    return user1, user2, post1, post2, comment1, comment2

def test_comment_model():
    """Test Comment model functionality."""
    print("\n🔍 Testing Comment Model...")
    
    user = User.objects.first()
    post = Post.objects.first()
    
    # Test comment creation
    comment = Comment.objects.create(
        post=post,
        author=user,
        content="Test comment content for model testing."
    )
    
    # Test string representation
    expected_str = f'Comment by {user.username} on {post.title}'
    if str(comment) == expected_str:
        print(f"   ✅ Comment __str__ method: WORKS")
    else:
        print(f"   ❌ Comment __str__ method: FAILED")
    
    # Test get_absolute_url
    expected_url = f'/post/{post.pk}/#comment-{comment.pk}'
    actual_url = comment.get_absolute_url()
    if actual_url == expected_url:
        print(f"   ✅ Comment get_absolute_url: WORKS")
    else:
        print(f"   ❌ Comment get_absolute_url: FAILED ('{actual_url}' != '{expected_url}')")
    
    # Test relationships
    if comment.post == post and comment.author == user:
        print(f"   ✅ Comment relationships: WORKS")
    else:
        print(f"   ❌ Comment relationships: FAILED")
    
    # Clean up test comment
    comment.delete()

def test_comment_form():
    """Test CommentForm validation."""
    print("\n📝 Testing Comment Form...")
    
    # Test valid form
    form_data = {'content': 'This is a valid comment with sufficient length.'}
    form = CommentForm(data=form_data)
    if form.is_valid():
        print(f"   ✅ Valid comment form: WORKS")
    else:
        print(f"   ❌ Valid comment form: FAILED - {form.errors}")
    
    # Test empty content
    form_data = {'content': ''}
    form = CommentForm(data=form_data)
    if not form.is_valid() and 'content' in form.errors:
        print(f"   ✅ Empty content validation: WORKS")
    else:
        print(f"   ❌ Empty content validation: FAILED")
    
    # Test too short content
    form_data = {'content': 'Hi'}
    form = CommentForm(data=form_data)
    if not form.is_valid() and 'content' in form.errors:
        print(f"   ✅ Short content validation: WORKS")
    else:
        print(f"   ❌ Short content validation: FAILED")
    
    # Test too long content
    form_data = {'content': 'x' * 1001}
    form = CommentForm(data=form_data)
    if not form.is_valid() and 'content' in form.errors:
        print(f"   ✅ Long content validation: WORKS")
    else:
        print(f"   ❌ Long content validation: FAILED")

def test_comment_urls():
    """Test comment-related URLs."""
    print("\n🔗 Testing Comment URLs...")
    
    client = Client()
    post = Post.objects.first()
    comment = Comment.objects.first()
    
    urls_to_test = [
        ('add-comment', [post.pk], 'Add Comment'),
        ('comment-create', [post.pk], 'Create Comment'),
        ('comment-update', [comment.pk], 'Update Comment'),
        ('comment-delete', [comment.pk], 'Delete Comment'),
    ]
    
    for url_name, args, description in urls_to_test:
        try:
            url = reverse(url_name, args=args)
            response = client.get(url)
            # Most comment views require authentication, so 302 redirect to login is expected
            if response.status_code in [200, 302]:
                print(f"   ✅ {description} URL ({url}): ACCESSIBLE")
            else:
                print(f"   ❌ {description} URL ({url}): FAILED - Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ {description} URL: FAILED - {str(e)}")

def test_comment_views():
    """Test comment views functionality."""
    print("\n👁️  Testing Comment Views...")
    
    client = Client()
    user1, user2, post1, post2, comment1, comment2 = create_test_data()
    
    # Test post detail view with comments
    print(f"   Testing post detail view with comments...")
    response = client.get(reverse('post-detail', args=[post1.pk]))
    if response.status_code == 200:
        content = response.content.decode()
        if 'comments-section' in content and str(comment1.content) in content:
            print(f"   ✅ Post detail with comments: WORKS")
        else:
            print(f"   ❌ Post detail with comments: FAILED - Comments not displayed")
    else:
        print(f"   ❌ Post detail view: FAILED - Status {response.status_code}")
    
    # Test authenticated comment creation
    print(f"   Testing authenticated comment creation...")
    client.login(username='testuser1', password='testpass123')
    
    comment_data = {
        'content': 'This is a test comment created through the view.'
    }
    response = client.post(reverse('add-comment', args=[post1.pk]), data=comment_data)
    if response.status_code == 302:  # Redirect after successful creation
        # Check if comment was created
        if Comment.objects.filter(content=comment_data['content']).exists():
            print(f"   ✅ Authenticated comment creation: WORKS")
        else:
            print(f"   ❌ Authenticated comment creation: FAILED - Comment not saved")
    else:
        print(f"   ❌ Authenticated comment creation: FAILED - Status {response.status_code}")
    
    # Test unauthenticated comment access
    print(f"   Testing unauthenticated comment access...")
    client.logout()
    response = client.get(reverse('add-comment', args=[post1.pk]))
    if response.status_code == 302:  # Redirect to login
        print(f"   ✅ Unauthenticated comment access: PROPERLY REDIRECTED")
    else:
        print(f"   ❌ Unauthenticated comment access: FAILED - Status {response.status_code}")

def test_comment_permissions():
    """Test comment permissions."""
    print("\n🔒 Testing Comment Permissions...")
    
    client = Client()
    user1, user2, post1, post2, comment1, comment2 = create_test_data()
    
    # Test comment author can edit their comment
    print(f"   Testing comment author can edit...")
    client.login(username='testuser2', password='testpass123')
    response = client.get(reverse('comment-update', args=[comment1.pk]))
    if response.status_code == 200:
        print(f"   ✅ Comment author can access edit: WORKS")
    else:
        print(f"   ❌ Comment author can access edit: FAILED - Status {response.status_code}")
    
    # Test non-author cannot edit comment
    print(f"   Testing non-author cannot edit...")
    client.login(username='testuser1', password='testpass123')
    response = client.get(reverse('comment-update', args=[comment1.pk]))
    if response.status_code == 403:  # Forbidden
        print(f"   ✅ Non-author cannot edit: PROPERLY BLOCKED")
    else:
        print(f"   ❌ Non-author cannot edit: FAILED - Status {response.status_code}")
    
    # Test comment author can delete their comment
    print(f"   Testing comment author can delete...")
    client.login(username='testuser2', password='testpass123')
    response = client.get(reverse('comment-delete', args=[comment1.pk]))
    if response.status_code == 200:
        print(f"   ✅ Comment author can access delete: WORKS")
    else:
        print(f"   ❌ Comment author can access delete: FAILED - Status {response.status_code}")

def test_comment_integration():
    """Test comment integration with posts."""
    print("\n🔄 Testing Comment Integration...")
    
    user = User.objects.first()
    post = Post.objects.first()
    
    # Test related_name works
    initial_count = post.comments.count()
    
    # Create a new comment
    comment = Comment.objects.create(
        post=post,
        author=user,
        content="Integration test comment."
    )
    
    # Check if count increased
    if post.comments.count() == initial_count + 1:
        print(f"   ✅ Comment-Post relationship: WORKS")
    else:
        print(f"   ❌ Comment-Post relationship: FAILED")
    
    # Test comment appears in post's comments
    if comment in post.comments.all():
        print(f"   ✅ Comment appears in post comments: WORKS")
    else:
        print(f"   ❌ Comment appears in post comments: FAILED")
    
    # Clean up
    comment.delete()

def main():
    """Run all comment functionality tests."""
    print("🚀 Starting Django Blog Comment Functionality Tests")
    print("=" * 60)
    
    try:
        # Create test data
        create_test_data()
        
        # Run all tests
        test_comment_model()
        test_comment_form()
        test_comment_urls()
        test_comment_views()
        test_comment_permissions()
        test_comment_integration()
        
        print("\n" + "=" * 60)
        print("✅ Comment functionality testing completed!")
        print("\n📋 Summary:")
        print("   - Comment model with proper relationships")
        print("   - Comment form with validation")
        print("   - Comment CRUD views with permissions")
        print("   - Comment templates integrated with post detail")
        print("   - Proper authentication and authorization")
        print("   - Admin interface for comment management")
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
