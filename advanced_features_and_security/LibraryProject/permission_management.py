#!/usr/bin/env python
"""
Permission Management Helper Script
This script shows how to manage custom permissions for users
"""

import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, UserProfile

def assign_permissions_by_role():
    """
    Example function showing how to assign book permissions based on user roles
    """
    
    print("=" * 60)
    print("PERMISSION ASSIGNMENT BY ROLE EXAMPLE")
    print("=" * 60)
    
    # Get the Book content type
    content_type = ContentType.objects.get_for_model(Book)
    
    # Get all custom book permissions
    can_add_book = Permission.objects.get(codename='can_add_book', content_type=content_type)
    can_change_book = Permission.objects.get(codename='can_change_book', content_type=content_type)
    can_delete_book = Permission.objects.get(codename='can_delete_book', content_type=content_type)
    
    print("\nAvailable Book Permissions:")
    print(f"- {can_add_book.name}")
    print(f"- {can_change_book.name}")
    print(f"- {can_delete_book.name}")
    
    # Example permission assignment by role
    print("\nRecommended Permission Assignment by Role:")
    print("-" * 50)
    
    print("👑 ADMIN Role:")
    print("  ✅ can_add_book")
    print("  ✅ can_change_book") 
    print("  ✅ can_delete_book")
    print("  → Full book management access")
    
    print("\n📚 LIBRARIAN Role:")
    print("  ✅ can_add_book")
    print("  ✅ can_change_book")
    print("  ❌ can_delete_book (optional)")
    print("  → Can manage books but deletion may be restricted")
    
    print("\n👤 MEMBER Role:")
    print("  ❌ can_add_book")
    print("  ❌ can_change_book")
    print("  ❌ can_delete_book")
    print("  → Read-only access to books")
    
    print("\nExample Code to Assign Permissions:")
    print("-" * 50)
    
    example_code = '''
# For Admin users
admin_user = User.objects.get(username='admin')
admin_user.user_permissions.add(can_add_book, can_change_book, can_delete_book)

# For Librarian users  
librarian_user = User.objects.get(username='librarian')
librarian_user.user_permissions.add(can_add_book, can_change_book)

# To check if user has permission
if admin_user.has_perm('relationship_app.can_add_book'):
    print("User can add books")
'''
    
    print(example_code)
    
    # Demonstrate permission checking
    print("\nTesting Permission Checking:")
    print("-" * 50)
    
    # Create a test user if it doesn't exist
    test_user, created = User.objects.get_or_create(
        username='permission_test_user',
        defaults={'password': 'testpass123'}
    )
    
    if created:
        print("✅ Created test user")
    
    # Check current permissions
    print(f"\nCurrent permissions for {test_user.username}:")
    if test_user.has_perm('relationship_app.can_add_book'):
        print("  ✅ can_add_book")
    else:
        print("  ❌ can_add_book")
        
    if test_user.has_perm('relationship_app.can_change_book'):
        print("  ✅ can_change_book")
    else:
        print("  ❌ can_change_book")
        
    if test_user.has_perm('relationship_app.can_delete_book'):
        print("  ✅ can_delete_book")
    else:
        print("  ❌ can_delete_book")
    
    # Assign permissions
    print(f"\nAssigning all book permissions to {test_user.username}...")
    test_user.user_permissions.add(can_add_book, can_change_book, can_delete_book)
    
    print("Permissions after assignment:")
    if test_user.has_perm('relationship_app.can_add_book'):
        print("  ✅ can_add_book")
    else:
        print("  ❌ can_add_book")
        
    if test_user.has_perm('relationship_app.can_change_book'):
        print("  ✅ can_change_book")
    else:
        print("  ❌ can_change_book")
        
    if test_user.has_perm('relationship_app.can_delete_book'):
        print("  ✅ can_delete_book")
    else:
        print("  ❌ can_delete_book")
    
    print("\n" + "=" * 60)
    print("Permission management example completed!")
    print("Use Django admin or custom management commands")
    print("to assign permissions to users in production.")
    print("=" * 60)

if __name__ == '__main__':
    assign_permissions_by_role()
