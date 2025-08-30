#!/usr/bin/env python
"""
Test script for Django Blog Authentication System
This script tests the authentication functionality including registration, login, and profile management.
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
from blog.forms import CustomUserCreationForm, UserUpdateForm

def test_authentication_system():
    """Test the authentication system functionality"""
    
    print("🔐 Testing Django Blog Authentication System")
    print("=" * 50)
    
    # Test 1: User Registration Form
    print("\n1. Testing User Registration Form...")
    form_data = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123'
    }
    
    form = CustomUserCreationForm(data=form_data)
    if form.is_valid():
        print("   ✅ Registration form validation: PASSED")
    else:
        print("   ❌ Registration form validation: FAILED")
        print(f"   Errors: {form.errors}")
    
    # Test 2: User Creation
    print("\n2. Testing User Creation...")
    try:
        # Create a test user
        test_user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User2'
        )
        print("   ✅ User creation: PASSED")
        print(f"   Created user: {test_user.username} ({test_user.email})")
    except Exception as e:
        print(f"   ❌ User creation: FAILED - {e}")
    
    # Test 3: User Update Form
    print("\n3. Testing User Update Form...")
    if 'test_user' in locals():
        update_form_data = {
            'username': 'testuser2',
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        update_form = UserUpdateForm(data=update_form_data, instance=test_user)
        if update_form.is_valid():
            print("   ✅ User update form validation: PASSED")
        else:
            print("   ❌ User update form validation: FAILED")
            print(f"   Errors: {update_form.errors}")
    
    # Test 4: URL Patterns
    print("\n4. Testing URL Patterns...")
    from django.urls import reverse, NoReverseMatch
    
    url_tests = [
        ('home', 'Home page'),
        ('posts', 'Posts list'),
        ('login', 'Login page'),
        ('logout', 'Logout page'),
        ('register', 'Registration page'),
        ('profile', 'Profile page')
    ]
    
    for url_name, description in url_tests:
        try:
            url = reverse(url_name)
            print(f"   ✅ {description} URL ({url_name}): {url}")
        except NoReverseMatch:
            print(f"   ❌ {description} URL ({url_name}): FAILED")
    
    # Test 5: Template Files Check
    print("\n5. Checking Template Files...")
    templates = [
        'blog/base.html',
        'blog/home.html',
        'blog/login.html',
        'blog/register.html',
        'blog/logout.html',
        'blog/profile.html',
        'blog/posts_list.html'
    ]
    
    for template in templates:
        template_path = os.path.join('blog', 'templates', template)
        if os.path.exists(template_path):
            print(f"   ✅ {template}: EXISTS")
        else:
            print(f"   ❌ {template}: MISSING")
    
    # Test 6: Form Fields Check
    print("\n6. Testing Form Fields...")
    
    # Check CustomUserCreationForm fields
    registration_form = CustomUserCreationForm()
    expected_fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    for field in expected_fields:
        if field in registration_form.fields:
            print(f"   ✅ Registration form field '{field}': EXISTS")
        else:
            print(f"   ❌ Registration form field '{field}': MISSING")
    
    # Check UserUpdateForm fields
    update_form = UserUpdateForm()
    expected_update_fields = ['username', 'first_name', 'last_name', 'email']
    
    for field in expected_update_fields:
        if field in update_form.fields:
            print(f"   ✅ Update form field '{field}': EXISTS")
        else:
            print(f"   ❌ Update form field '{field}': MISSING")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication System Test Complete!")
    print("\nNext Steps:")
    print("1. Visit http://127.0.0.1:8000/ to test the live application")
    print("2. Try registering a new user")
    print("3. Test login/logout functionality")
    print("4. Update user profile information")
    print("5. Verify CSRF protection is working")

if __name__ == '__main__':
    test_authentication_system()
