#!/usr/bin/env python
"""
Comprehensive Permission Testing Script

This script implements Step 4 of the permission management task:
- Creates test users and assigns them to different groups
- Tests that permissions are enforced correctly
- Verifies that users can only access views they have permissions for

Run this script to verify your permissions implementation works correctly.
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group
from bookshelf.models import CustomUser, Book
from django.test import Client
from django.urls import reverse
import sys

def create_test_users():
    """Create test users and assign them to groups"""
    print("🔧 Setting up test users...")
    
    # Clean up existing test users
    CustomUser.objects.filter(username__startswith='test_').delete()
    
    # Create test users
    viewer_user = CustomUser.objects.create_user(
        username='test_viewer',
        email='viewer@test.com', 
        password='testpass123'
    )
    
    editor_user = CustomUser.objects.create_user(
        username='test_editor',
        email='editor@test.com',
        password='testpass123'
    )
    
    admin_user = CustomUser.objects.create_user(
        username='test_admin',
        email='admin@test.com',
        password='testpass123'
    )
    
    # Assign users to groups
    viewers_group = Group.objects.get(name='Viewers')
    editors_group = Group.objects.get(name='Editors')
    admins_group = Group.objects.get(name='Admins')
    
    viewer_user.groups.add(viewers_group)
    editor_user.groups.add(editors_group)
    admin_user.groups.add(admins_group)
    
    print("✅ Test users created and assigned to groups")
    return viewer_user, editor_user, admin_user

def create_test_book():
    """Create a test book for testing operations"""
    book, created = Book.objects.get_or_create(
        title='Test Book',
        defaults={
            'author': 'Test Author',
            'publication_year': 2024
        }
    )
    return book

def test_permissions():
    """Test permission enforcement in views"""
    print("\n🧪 Testing Permission Enforcement...")
    print("=" * 60)
    
    # Create test users
    viewer_user, editor_user, admin_user = create_test_users()
    
    # Create test book
    test_book = create_test_book()
    
    # Test scenarios for each user type
    users_to_test = [
        (viewer_user, 'Viewer'),
        (editor_user, 'Editor'), 
        (admin_user, 'Admin')
    ]
    
    # URLs to test with their required permissions
    urls_to_test = [
        ('book_list', 'can_view', '/bookshelf/books/'),
        ('book_create', 'can_create', '/bookshelf/books/create/'),
        ('book_edit', 'can_edit', f'/bookshelf/books/{test_book.id}/edit/'),
        ('book_delete', 'can_delete', f'/bookshelf/books/{test_book.id}/delete/'),
    ]
    
    client = Client()
    
    print(f"{'User':<12} {'URL':<20} {'Permission':<12} {'Expected':<10} {'Result':<10}")
    print("-" * 80)
    
    for user, role in users_to_test:
        for url_name, permission, url_path in urls_to_test:
            # Login as the test user
            client.login(username=user.username, password='testpass123')
            
            # Check if user has the required permission
            has_permission = user.has_perm(f'bookshelf.{permission}')
            expected = "✅ Allow" if has_permission else "❌ Deny"
            
            try:
                if url_name == 'book_edit' or url_name == 'book_delete':
                    response = client.get(url_path)
                else:
                    response = client.get(url_path)
                
                if response.status_code == 200:
                    result = "✅ Access"
                elif response.status_code == 403:
                    result = "❌ Denied"
                elif response.status_code == 302:
                    result = "🔄 Redirect"
                else:
                    result = f"⚠️  {response.status_code}"
                    
            except Exception as e:
                result = f"❗ Error"
            
            print(f"{role:<12} {url_name:<20} {permission:<12} {expected:<10} {result:<10}")
            
            # Logout after each test
            client.logout()
    
    print("\n📊 Permission Test Summary:")
    print("✅ Access = User successfully accessed the view")
    print("❌ Denied = User was correctly denied access (403 Forbidden)")  
    print("🔄 Redirect = User was redirected (usually to login)")
    print("⚠️  = Unexpected response code")
    
    # Cleanup
    CustomUser.objects.filter(username__startswith='test_').delete()
    print("\n🧹 Cleaned up test users")

def verify_group_permissions():
    """Verify that groups have the correct permissions assigned"""
    print("\n🔍 Verifying Group Permissions...")
    print("=" * 40)
    
    expected_permissions = {
        'Viewers': ['can_view'],
        'Editors': ['can_view', 'can_create', 'can_edit'],
        'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete']
    }
    
    for group_name, expected_perms in expected_permissions.items():
        try:
            group = Group.objects.get(name=group_name)
            actual_perms = [p.codename for p in group.permissions.all()]
            
            missing_perms = set(expected_perms) - set(actual_perms)
            extra_perms = set(actual_perms) - set(expected_perms)
            
            print(f"\n{group_name} Group:")
            print(f"  Expected: {expected_perms}")
            print(f"  Actual:   {actual_perms}")
            
            if not missing_perms and not extra_perms:
                print(f"  Status:   ✅ Correct")
            else:
                print(f"  Status:   ❌ Issues found")
                if missing_perms:
                    print(f"  Missing:  {list(missing_perms)}")
                if extra_perms:
                    print(f"  Extra:    {list(extra_perms)}")
                    
        except Group.DoesNotExist:
            print(f"❌ Group '{group_name}' not found!")

def main():
    """Main function to run all tests"""
    print("🚀 Starting Permission System Testing")
    print("=" * 60)
    
    try:
        # Verify groups and permissions are set up correctly  
        verify_group_permissions()
        
        # Test permission enforcement in views
        test_permissions()
        
        print("\n✅ Permission testing completed successfully!")
        print("\n📝 Next Steps:")
        print("1. Check the results above to ensure permissions work as expected")
        print("2. Log into Django admin to manage users and groups")  
        print("3. Test manually by logging in as different users")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()