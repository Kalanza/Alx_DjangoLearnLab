# Library Management System - Permissions & Groups Implementation

## Overview
This Django application implements a comprehensive permissions and groups system for managing access to book operations. The system demonstrates role-based access control (RBAC) with custom permissions, user groups, and view-level security.

## Custom Permissions Implementation

### Step 1: Model Permissions (`bookshelf/models.py`)

The `Book` model includes custom permissions that control four core operations:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

**Permission Definitions:**
- `can_view`: Allows viewing book lists and individual book details
- `can_create`: Allows creating new books in the system
- `can_edit`: Allows modifying existing book information
- `can_delete`: Allows removing books from the system

## Groups and Permission Assignments

### Step 2: User Groups Configuration

Three distinct user groups have been implemented with specific permission sets:

#### 1. **Viewers Group**
- **Permissions:** `can_view`
- **Purpose:** Read-only access to books
- **Use Case:** Library visitors, students, general users

#### 2. **Editors Group**  
- **Permissions:** `can_create`, `can_edit`
- **Purpose:** Content management without deletion rights
- **Use Case:** Library staff, content managers

#### 3. **Admins Group**
- **Permissions:** `can_view`, `can_create`, `can_edit`, `can_delete`
- **Purpose:** Full administrative access
- **Use Case:** System administrators, head librarians

### Automated Group Setup

Groups are created automatically using the management command:

```bash
python manage.py setup_groups
```

This command (`bookshelf/management/commands/setup_groups.py`) creates groups and assigns permissions programmatically.

## View-Level Permission Enforcement

### Step 3: Protected Views (`bookshelf/views.py`)

Each view is protected with the `@permission_required` decorator:

```python
# View Books - Requires can_view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_view', raise_exception=True)  
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Create Books - Requires can_create permission
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    # Book creation logic
    return render(request, 'bookshelf/book_form.html', {'form_title': 'Create Book'})

# Edit Books - Requires can_edit permission
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # Book editing logic
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_form.html', {'book': book})

# Delete Books - Requires can_delete permission
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    # Book deletion logic
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
```

**Permission Format:** `'app_name.permission_code'`
- App name: `bookshelf`
- Permission codes: `can_view`, `can_create`, `can_edit`, `can_delete`

## Template-Level Permission Checks

Views dynamically show/hide UI elements based on user permissions:

```html
<!-- Navigation - Only show create button to authorized users -->
{% if perms.bookshelf.can_create %}
    <a href="{% url 'book_create' %}">Add New Book</a>
{% endif %}

<!-- Book Actions - Conditional button display -->
{% if perms.bookshelf.can_view %}
    <a href="{% url 'book_detail' book.pk %}">View</a>
{% endif %}

{% if perms.bookshelf.can_edit %}
    <a href="{% url 'book_edit' book.pk %}">Edit</a>
{% endif %}

{% if perms.bookshelf.can_delete %}
    <a href="{% url 'book_delete' book.pk %}">Delete</a>
{% endif %}
```

## System Setup Instructions

### 1. Database Migration
```bash
# Create and apply migrations for custom permissions
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Groups and Permissions
```bash
# Run the automated setup command
python manage.py setup_groups
```

### 3. Create Test Users
```bash
# Create superuser for admin access
python manage.py createsuperuser

# Test users are created programmatically with sample data
```

## Testing the Permission System

### Test Users Created
- **viewer_user** (password: testpass123) - Viewers group
- **editor_user** (password: testpass123) - Editors group
- **admin_user** (password: testpass123) - Admins group

### Testing Scenarios

#### Viewer Access Test:
1. Login as `viewer_user`
2. Navigate to `/bookshelf/books/`
3. **Expected:** Can see book list, no create/edit/delete buttons
4. **Test direct access:** Visit `/bookshelf/books/create/`
5. **Expected:** Permission denied error

#### Editor Access Test:
1. Login as `editor_user`
2. Navigate to `/bookshelf/books/`
3. **Expected:** Can see create and edit buttons, no delete buttons
4. **Test creation:** Use "Add New Book" feature
5. **Test editing:** Modify existing book information
6. **Test direct access:** Visit `/bookshelf/books/1/delete/`
7. **Expected:** Permission denied error

#### Admin Access Test:
1. Login as `admin_user`
2. Navigate to `/bookshelf/books/`
3. **Expected:** Full access to all operations
4. **Test all CRUD operations:** Create, view, edit, delete books

## URL Patterns and Permission Requirements

```python
# URL patterns with their required permissions
urlpatterns = [
    path('books/', views.book_list, name='book_list'),                    # can_view
    path('books/<int:pk>/', views.book_detail, name='book_detail'),       # can_view
    path('books/create/', views.book_create, name='book_create'),         # can_create
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),      # can_edit
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'), # can_delete
]
```

## Security Features Implemented

### 1. Multi-Layer Protection
- **View-level:** `@permission_required` decorators
- **Template-level:** `{% if perms.app.permission %}` checks
- **URL-level:** Direct access blocked for unauthorized users

### 2. Exception Handling
- `raise_exception=True` ensures proper error responses
- Unauthorized access returns HTTP 403 Forbidden
- Clear error messages for debugging

### 3. Group-Based Management
- Easy user role assignment through Django admin
- Scalable permission management
- Centralized access control

## Custom User Model Integration

The system integrates with a custom user model (`CustomUser`) that includes:
- Extended user fields (date_of_birth, profile_photo)
- Custom user manager for creation/management
- User profiles with role assignments
- Automatic profile creation via Django signals

## Administrative Features

### Django Admin Integration
- Custom admin classes for user and book management
- Group and permission management through admin interface
- User assignment to groups via admin panel

### Management Commands
- `setup_groups`: Automated group and permission creation
- Extensible command structure for future automation needs

## File Structure

```
LibraryProject/
├── bookshelf/
│   ├── models.py                 # Book model with custom permissions
│   ├── views.py                  # Permission-protected views
│   ├── admin.py                  # Admin configuration
│   ├── urls.py                   # URL patterns
│   ├── templates/bookshelf/      # Permission-aware templates
│   └── management/commands/
│       └── setup_groups.py       # Automated setup command
├── PERMISSIONS_README.md         # Detailed technical documentation
└── README.md                     # This file - Setup and usage guide
```

## Production Considerations

1. **Remove debug information** from templates (permission display section)
2. **Implement logging** for permission denied attempts
3. **Add permission caching** for high-traffic scenarios
4. **Consider object-level permissions** for fine-grained control
5. **Implement API permissions** if REST API is added

## Extension Guidelines

To add permissions to other models:

1. **Define permissions in model Meta class**
2. **Create protected views with decorators**
3. **Update management command to include new permissions**
4. **Add template permission checks**
5. **Update group assignments as needed**

This implementation provides a robust, scalable foundation for role-based access control in Django applications.
