"""
Django management command to set up groups and permissions for the Library Management System.

This command creates the following groups with their respective permissions:
- Editors: can_create, can_edit
- Viewers: can_view  
- Admins: can_view, can_create, can_edit, can_delete

Usage: python manage.py setup_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create user groups and assign permissions for the Library Management System'

    def handle(self, *args, **options):
        # Get the content type for Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create permissions
        permissions = {}
        permission_codenames = ['can_view', 'can_create', 'can_edit', 'can_delete']
        
        for codename in permission_codenames:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=book_content_type,
                defaults={'name': f'Can {codename.split("_")[1]} book'}
            )
            permissions[codename] = permission
            if created:
                self.stdout.write(f'Created permission: {permission}')
            else:
                self.stdout.write(f'Permission already exists: {permission}')

        # Create groups and assign permissions
        group_permissions = {
            'Editors': ['can_create', 'can_edit'],
            'Viewers': ['can_view'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete']
        }

        for group_name, permission_codenames in group_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(f'Created group: {group_name}')
            else:
                self.stdout.write(f'Group already exists: {group_name}')
            
            # Clear existing permissions and add new ones
            group.permissions.clear()
            for codename in permission_codenames:
                group.permissions.add(permissions[codename])
            
            self.stdout.write(f'Assigned permissions to {group_name}: {", ".join(permission_codenames)}')

        self.stdout.write(
            self.style.SUCCESS(
                '\nGroups and permissions setup completed successfully!\n'
                '\nNext steps:\n'
                '1. Create test users in the Django admin\n'
                '2. Assign users to groups\n'
                '3. Test the permission system by logging in as different users\n'
                '\nAccess the application at: /bookshelf/books/'
            )
        )
