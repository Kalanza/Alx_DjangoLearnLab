#!/usr/bin/env python
"""
Script to set up groups and permissions for the Django application.
This implements Step 2 of the permissions and groups management task.
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

def setup_groups_and_permissions():
    """
    Create groups and assign appropriate permissions to each group.
    """
    
    # Get the Book content type
    book_content_type = ContentType.objects.get_for_model(Book)
    
    # Get or create custom permissions for Book model
    can_view, created = Permission.objects.get_or_create(
        codename='can_view',
        name='Can view book',
        content_type=book_content_type,
    )
    
    can_create, created = Permission.objects.get_or_create(
        codename='can_create',
        name='Can create book',
        content_type=book_content_type,
    )
    
    can_edit, created = Permission.objects.get_or_create(
        codename='can_edit',
        name='Can edit book',
        content_type=book_content_type,
    )
    
    can_delete, created = Permission.objects.get_or_create(
        codename='can_delete',
        name='Can delete book',
        content_type=book_content_type,
    )
    
    # Create Groups and assign permissions
    
    # 1. Viewers Group - Can only view books
    viewers_group, created = Group.objects.get_or_create(name='Viewers')
    if created:
        print("Created 'Viewers' group")
    viewers_group.permissions.set([can_view])
    print(f"Assigned permissions to Viewers: {[p.name for p in viewers_group.permissions.all()]}")
    
    # 2. Editors Group - Can view, create, and edit books (but not delete)
    editors_group, created = Group.objects.get_or_create(name='Editors')
    if created:
        print("Created 'Editors' group")  
    editors_group.permissions.set([can_view, can_create, can_edit])
    print(f"Assigned permissions to Editors: {[p.name for p in editors_group.permissions.all()]}")
    
    # 3. Admins Group - Full permissions (view, create, edit, delete)
    admins_group, created = Group.objects.get_or_create(name='Admins')
    if created:
        print("Created 'Admins' group")
    admins_group.permissions.set([can_view, can_create, can_edit, can_delete])
    print(f"Assigned permissions to Admins: {[p.name for p in admins_group.permissions.all()]}")
    
    print("\n✅ Groups and permissions setup completed successfully!")
    
    # Display summary
    print("\n📋 SUMMARY:")
    print("=" * 50)
    for group in Group.objects.filter(name__in=['Viewers', 'Editors', 'Admins']):
        permissions_list = [p.name for p in group.permissions.all()]
        print(f"{group.name}: {', '.join(permissions_list)}")

if __name__ == '__main__':
    setup_groups_and_permissions()