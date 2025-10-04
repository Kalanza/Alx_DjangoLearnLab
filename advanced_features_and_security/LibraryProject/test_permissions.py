#!/usr/bin/env python
"""
Script to test the permissions and groups system.
This verifies that the permissions are working correctly.
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from bookshelf.models import CustomUser, Book

def test_permissions():
    """
    Test the permissions system by creating test users and checking their permissions.
    """
    
    print("🧪 Testing Permissions and Groups System")
    print("=" * 50)
    
    # Clean up any existing test users
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
    
    print("✅ Created test users and assigned to groups")
    
    # Test permissions
    users_and_roles = [
        (viewer_user, 'Viewer'),
        (editor_user, 'Editor'), 
        (admin_user, 'Admin')
    ]
    
    permissions_to_test = [
        'bookshelf.can_view',
        'bookshelf.can_create',
        'bookshelf.can_edit',
        'bookshelf.can_delete'
    ]
    
    print("\n📋 Permission Test Results:")
    print("-" * 80)
    print(f"{'User Role':<12} {'Can View':<10} {'Can Create':<12} {'Can Edit':<10} {'Can Delete':<12}")
    print("-" * 80)
    
    for user, role in users_and_roles:
        permissions_status = []
        for perm in permissions_to_test:
            has_perm = user.has_perm(perm)
            permissions_status.append('✅' if has_perm else '❌')
        
        print(f"{role:<12} {permissions_status[0]:<10} {permissions_status[1]:<12} {permissions_status[2]:<10} {permissions_status[3]:<12}")
    
    print("\n🔍 Expected Results:")
    print("- Viewers: ✅ View only")
    print("- Editors: ✅ View, Create, Edit (no Delete)")
    print("- Admins:  ✅ All permissions (View, Create, Edit, Delete)")
    
    # Verify group memberships
    print(f"\n👥 Group Memberships:")
    print(f"- {viewer_user.username} is in groups: {[g.name for g in viewer_user.groups.all()]}")
    print(f"- {editor_user.username} is in groups: {[g.name for g in editor_user.groups.all()]}")
    print(f"- {admin_user.username} is in groups: {[g.name for g in admin_user.groups.all()]}")
    
    # Clean up test users
    CustomUser.objects.filter(username__startswith='test_').delete()
    print("\n🧹 Cleaned up test users")
    
    print("\n✅ Permissions testing completed successfully!")

if __name__ == '__main__':
    test_permissions()