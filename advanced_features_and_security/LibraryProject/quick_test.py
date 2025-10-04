#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group
from bookshelf.models import CustomUser

print('=== STEP 4: PERMISSION TESTING ===')

# Clean and create test users
CustomUser.objects.filter(username__startswith='test_').delete()
viewer = CustomUser.objects.create_user('test_viewer', 'viewer@test.com', 'pass123')
editor = CustomUser.objects.create_user('test_editor', 'editor@test.com', 'pass123')
admin = CustomUser.objects.create_user('test_admin', 'admin@test.com', 'pass123')

# Assign to groups
viewer.groups.add(Group.objects.get(name='Viewers'))
editor.groups.add(Group.objects.get(name='Editors'))
admin.groups.add(Group.objects.get(name='Admins'))

print('✅ Test users created and assigned to groups')

# Test permissions
print('\nPermission Test Results:')
print(f'Viewer - view: {viewer.has_perm("bookshelf.can_view")}, create: {viewer.has_perm("bookshelf.can_create")}, edit: {viewer.has_perm("bookshelf.can_edit")}, delete: {viewer.has_perm("bookshelf.can_delete")}')
print(f'Editor - view: {editor.has_perm("bookshelf.can_view")}, create: {editor.has_perm("bookshelf.can_create")}, edit: {editor.has_perm("bookshelf.can_edit")}, delete: {editor.has_perm("bookshelf.can_delete")}')
print(f'Admin - view: {admin.has_perm("bookshelf.can_view")}, create: {admin.has_perm("bookshelf.can_create")}, edit: {admin.has_perm("bookshelf.can_edit")}, delete: {admin.has_perm("bookshelf.can_delete")}')

# Cleanup
CustomUser.objects.filter(username__startswith='test_').delete()
print('\n✅ Step 4 completed: Permissions tested successfully!')