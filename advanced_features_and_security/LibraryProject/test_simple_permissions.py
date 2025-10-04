#!/usr/bin/env python
"""
Simple Permission Test - Step 4 Implementation

This script creates test users, assigns them to groups, and verifies 
that they have the correct permissions without using the test client.
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group
from bookshelf.models import CustomUser, Book

def test_user_permissions():
    """Test that users in different groups have correct permissions"""
    print("🧪 Testing User Permissions (Step 4)")
    print("=" * 50)
    
    # Clean up existing test users
    CustomUser.objects.filter(username__startswith='test_').delete()
    print("🧹 Cleaned up existing test users")
    
    # Create test users
    viewer = CustomUser.objects.create_user('test_viewer', 'viewer@test.com', 'pass123')
    editor = CustomUser.objects.create_user('test_editor', 'editor@test.com', 'pass123')
    admin = CustomUser.objects.create_user('test_admin', 'admin@test.com', 'pass123')
    
    # Assign to groups
    viewer.groups.add(Group.objects.get(name='Viewers'))
    editor.groups.add(Group.objects.get(name='Editors'))
    admin.groups.add(Group.objects.get(name='Admins'))
    
    print("✅ Created test users and assigned to groups")
    
    # Test permissions
    users = [
        (viewer, 'Viewer'),
        (editor, 'Editor'),
        (admin, 'Admin')
    ]
    
    permissions = ['can_view', 'can_create', 'can_edit', 'can_delete']
    
    print(f"\n📋 Permission Test Results:")
    print(f"{'User':<12} {'can_view':<10} {'can_create':<12} {'can_edit':<10} {'can_delete':<12}")
    print("-" * 70)
    
    for user, role in users:
        perm_results = []
        for perm in permissions:
            has_perm = user.has_perm(f'bookshelf.{perm}')
            perm_results.append('✅' if has_perm else '❌')
        
        print(f"{role:<12} {perm_results[0]:<10} {perm_results[1]:<12} {perm_results[2]:<10} {perm_results[3]:<12}")
    
    # Verify expected behavior
    print(f"\n🔍 Verification:")
    
    # Test Viewer (should only have can_view)
    viewer_perms = {
        'can_view': viewer.has_perm('bookshelf.can_view'),
        'can_create': viewer.has_perm('bookshelf.can_create'),
        'can_edit': viewer.has_perm('bookshelf.can_edit'),
        'can_delete': viewer.has_perm('bookshelf.can_delete')
    }
    
    if viewer_perms == {'can_view': True, 'can_create': False, 'can_edit': False, 'can_delete': False}:
        print("✅ Viewer permissions correct")
    else:
        print("❌ Viewer permissions incorrect")
    
    # Test Editor (should have view, create, edit but not delete)
    editor_perms = {
        'can_view': editor.has_perm('bookshelf.can_view'),
        'can_create': editor.has_perm('bookshelf.can_create'),
        'can_edit': editor.has_perm('bookshelf.can_edit'),
        'can_delete': editor.has_perm('bookshelf.can_delete')
    }
    
    if editor_perms == {'can_view': True, 'can_create': True, 'can_edit': True, 'can_delete': False}:
        print("✅ Editor permissions correct")
    else:
        print("❌ Editor permissions incorrect")
    
    # Test Admin (should have all permissions)
    admin_perms = {
        'can_view': admin.has_perm('bookshelf.can_view'),
        'can_create': admin.has_perm('bookshelf.can_create'),
        'can_edit': admin.has_perm('bookshelf.can_edit'),
        'can_delete': admin.has_perm('bookshelf.can_delete')
    }
    
    if admin_perms == {'can_view': True, 'can_create': True, 'can_edit': True, 'can_delete': True}:
        print("✅ Admin permissions correct")
    else:
        print("❌ Admin permissions incorrect")
    
    # Show group memberships
    print(f"\n👥 Group Memberships:")
    for user, role in users:
        groups = [g.name for g in user.groups.all()]
        print(f"- {role}: {groups}")
    
    # Clean up
    CustomUser.objects.filter(username__startswith='test_').delete()
    print(f"\n🧹 Test users cleaned up")
    
    print(f"\n✅ Permission testing completed!")
    print(f"\n📝 Manual Testing Instructions:")
    print(f"1. Create users via Django admin: /admin/")
    print(f"2. Assign users to Viewers, Editors, or Admins groups")
    print(f"3. Test access to these URLs:")
    print(f"   - /bookshelf/books/ (requires can_view)")
    print(f"   - /bookshelf/books/create/ (requires can_create)")
    print(f"   - /bookshelf/books/1/edit/ (requires can_edit)")
    print(f"   - /bookshelf/books/1/delete/ (requires can_delete)")

if __name__ == '__main__':
    test_user_permissions()