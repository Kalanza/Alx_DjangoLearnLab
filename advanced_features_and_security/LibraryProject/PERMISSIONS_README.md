# Django Permissions and Groups Implementation

## Overview
This implementation demonstrates Django's permissions and groups system for controlling access to book management functionality in a library application.

## Custom Permissions Implemented

### Book Model Permissions
The following custom permissions are defined in `bookshelf/models.py`:

- `can_view`: Allow viewing book details and list
- `can_create`: Allow creating new books  
- `can_edit`: Allow editing existing books
- `can_delete`: Allow deleting books

## Groups and Permission Assignments

### 1. Viewers Group
**Permissions**: `can_view`
**Purpose**: Users can only view books, no modification rights
**Use Case**: Library visitors, students with read-only access

### 2. Editors Group  
**Permissions**: `can_create`, `can_edit`
**Purpose**: Users can add and modify books but cannot delete
**Use Case**: Library staff, content editors

### 3. Admins Group
**Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
**Purpose**: Full access to all book operations
**Use Case**: Library administrators, system admins

## Implementation Details

### Models (`bookshelf/models.py`)
```python
class Book(models.Model):
    # ... fields ...
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"), 
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

### Views (`bookshelf/views.py`)
Each view is protected with the `@permission_required` decorator:

- `book_list()`: Requires `bookshelf.can_view`
- `book_detail()`: Requires `bookshelf.can_view`
- `book_create()`: Requires `bookshelf.can_create`
- `book_edit()`: Requires `bookshelf.can_edit`
- `book_delete()`: Requires `bookshelf.can_delete`

### Templates
Templates use `{% if perms.bookshelf.permission_name %}` to conditionally show/hide UI elements based on user permissions.

## Setup Instructions

### 1. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Set Up Groups and Permissions
```bash
python manage.py setup_groups
```

### 3. Create Test Users
1. Access Django admin: `http://localhost:8000/admin/`
2. Create users with different roles
3. Assign users to appropriate groups

### 4. Test the System
Access the application at: `http://localhost:8000/bookshelf/books/`

## Testing Guide

### Test Users to Create:

1. **viewer_user**
   - Add to "Viewers" group
   - Should only see books, no create/edit/delete buttons

2. **editor_user**  
   - Add to "Editors" group
   - Can create and edit books, but cannot delete

3. **admin_user**
   - Add to "Admins" group  
   - Full access to all operations

### Testing Steps:

1. **Test Viewer Access**:
   - Login as viewer_user
   - Visit `/bookshelf/books/`
   - Verify: Can see book list, cannot see "Add New Book" button
   - Try accessing `/bookshelf/books/create/` directly → Should get permission denied

2. **Test Editor Access**:
   - Login as editor_user  
   - Verify: Can create and edit books
   - Try accessing delete URL directly → Should get permission denied

3. **Test Admin Access**:
   - Login as admin_user
   - Verify: Full access to all operations

## URL Patterns

- `/bookshelf/books/` - Book list (requires can_view)
- `/bookshelf/books/<id>/` - Book detail (requires can_view)
- `/bookshelf/books/create/` - Create book (requires can_create)
- `/bookshelf/books/<id>/edit/` - Edit book (requires can_edit)
- `/bookshelf/books/<id>/delete/` - Delete book (requires can_delete)

## Permission Enforcement

### View-Level Protection
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # View logic here
```

### Template-Level Protection  
```html
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Add New Book</a>
{% endif %}
```

## Security Features

1. **Decorator Protection**: All views use `@permission_required` decorator
2. **Template Conditional Rendering**: UI elements only shown to authorized users
3. **Automatic Exception Handling**: Unauthorized access raises PermissionDenied
4. **Group-Based Management**: Easy to assign users to roles
5. **Granular Permissions**: Separate permissions for each operation

## Management Commands

- `python manage.py setup_groups`: Automatically creates groups and assigns permissions

This implementation provides a complete, secure permissions system that can be easily extended for other models and operations.
