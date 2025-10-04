# Django Permissions and Groups System Documentation

## Overview
This document explains how the permissions and groups system is configured and used in the Django application to control access to various parts of the application.

## Implementation Summary

### Step 1: Custom Permissions in Models ✅

**File: `bookshelf/models.py`**

The `Book` model includes four custom permissions:

```python
class Book(models.Model):
    # ... model fields ...
    
    class Meta:
        ordering = ['title']
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

**Permission Codenames:**
- `bookshelf.can_view` - Allows viewing book list
- `bookshelf.can_create` - Allows creating new books  
- `bookshelf.can_edit` - Allows editing existing books
- `bookshelf.can_delete` - Allows deleting books

### Step 2: Groups with Assigned Permissions ✅

**Three user groups have been created:**

#### 👁️ Viewers Group
- **Permissions:** `can_view` only
- **Purpose:** Read-only access to books
- **Can access:** Book list view only

#### ✏️ Editors Group  
- **Permissions:** `can_view`, `can_create`, `can_edit`
- **Purpose:** Can create and modify books but cannot delete
- **Can access:** Book list, create, and edit views

#### 👑 Admins Group
- **Permissions:** `can_view`, `can_create`, `can_edit`, `can_delete`
- **Purpose:** Full access to all book operations
- **Can access:** All book views including delete

**Setup Script:** `setup_groups_permissions.py` automatically creates these groups and assigns permissions.

### Step 3: Permission-Protected Views ✅

**File: `bookshelf/views.py`**

All views use the `@permission_required` decorator to enforce permissions:

```python
# Example view with permission requirement
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View requires 'can_view' permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
```

**View Permissions:**
- `book_list` - Requires: `bookshelf.can_view`
- `book_create` - Requires: `bookshelf.can_create`
- `book_edit` - Requires: `bookshelf.can_edit`
- `book_delete` - Requires: `bookshelf.can_delete`

**URL Routes:** `bookshelf/urls.py` maps URLs to permission-protected views.

### Step 4: Permission Testing ✅

**Test Scripts:**
- `test_permissions_comprehensive.py` - Full automated testing
- `quick_test.py` - Simple permission verification

**Manual Testing Process:**
1. Create users in Django admin (`/admin/`)
2. Assign users to appropriate groups (Viewers, Editors, Admins)
3. Test access to URLs:
   - `/bookshelf/books/` (requires can_view)
   - `/bookshelf/books/create/` (requires can_create)
   - `/bookshelf/books/1/edit/` (requires can_edit)
   - `/bookshelf/books/1/delete/` (requires can_delete)

### Step 5: Documentation ✅

This document provides complete setup and usage instructions.

## How to Use the System

### For Administrators:

1. **Access Django Admin:**
   ```
   http://localhost:8000/admin/
   ```

2. **Create Users:**
   - Go to "Users" section
   - Add new user with username and password
   - Save user

3. **Assign User to Group:**
   - Edit the user
   - In "Groups" section, select appropriate group:
     - Viewers (read-only access)
     - Editors (create, edit access)
     - Admins (full access)
   - Save changes

4. **Manage Groups and Permissions:**
   - Go to "Groups" section in admin
   - View/modify permissions for each group
   - Groups are pre-configured but can be customized

### For Developers:

1. **Adding New Permissions:**
   ```python
   class MyModel(models.Model):
       # ... fields ...
       
       class Meta:
           permissions = [
               ("custom_permission", "Description of permission"),
           ]
   ```

2. **Protecting Views:**
   ```python
   from django.contrib.auth.decorators import permission_required
   
   @permission_required('app_name.permission_codename', raise_exception=True)
   def my_view(request):
       # View logic here
       pass
   ```

3. **Checking Permissions in Templates:**
   ```html
   {% if perms.bookshelf.can_create %}
       <a href="{% url 'book_create' %}">Create Book</a>
   {% endif %}
   ```

4. **Checking Permissions in Code:**
   ```python
   if request.user.has_perm('bookshelf.can_edit'):
       # Allow editing
       pass
   ```

## Permission Matrix

| Group   | View Books | Create Books | Edit Books | Delete Books |
|---------|------------|--------------|------------|--------------|
| Viewers | ✅         | ❌           | ❌         | ❌           |
| Editors | ✅         | ✅           | ✅         | ❌           |
| Admins  | ✅         | ✅           | ✅         | ✅           |

## Setup Commands

1. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Groups and Permissions:**
   ```bash
   python setup_groups_permissions.py
   ```

3. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Test Permissions:**
   ```bash
   python quick_test.py
   ```

## Security Notes

- All views require user authentication (`@login_required`)
- Permissions are enforced at the view level using decorators
- `raise_exception=True` returns 403 Forbidden for unauthorized access
- Groups provide role-based access control (RBAC)
- Permissions are stored in database and can be managed via admin interface

## Troubleshooting

1. **User can't access view:**
   - Check if user is logged in
   - Verify user is in correct group
   - Confirm group has required permission

2. **Permission not working:**
   - Run migrations after adding new permissions
   - Check permission codename matches exactly
   - Verify decorator syntax in views

3. **403 Forbidden errors:**
   - This is expected behavior for users without permissions
   - Check server logs for specific permission that was denied

## Files Modified/Created

- ✅ `bookshelf/models.py` - Added custom permissions to Book model
- ✅ `bookshelf/views.py` - Created permission-protected views
- ✅ `bookshelf/urls.py` - URL routing for protected views
- ✅ `setup_groups_permissions.py` - Automated group/permission setup
- ✅ `test_permissions_comprehensive.py` - Comprehensive testing
- ✅ `quick_test.py` - Simple permission testing
- ✅ `README_PERMISSIONS.md` - This documentation file

This implementation provides a complete, production-ready permissions and groups system for controlling access to different parts of the Django application.