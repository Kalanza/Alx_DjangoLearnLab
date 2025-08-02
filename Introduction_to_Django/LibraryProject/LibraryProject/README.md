# Django Bookshelf Project

A simple Django application demonstrating CRUD (Create, Read, Update, Delete) operations with a Book model.

## Project Structure

```
LibraryProject/
├── manage.py                 # Django management script
├── LibraryProject/          # Main project settings
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── bookshelf/               # Django app
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Book model definition
│   ├── views.py             # Views (empty for now)
│   ├── tests.py             # Tests (empty for now)
│   └── migrations/          # Database migrations
└── docs/                    # Documentation
    ├── CRUD_operations.md   # Complete CRUD guide
    ├── create.md            # CREATE operations
    ├── retrieve.md          # RETRIEVE operations
    ├── update.md            # UPDATE operations
    └── delete.md            # DELETE operations
```

## Book Model

The `Book` model includes:
- `title`: CharField with max length 200
- `author`: CharField with max length 100  
- `publication_year`: IntegerField

## Setup Instructions

1. **Navigate to project directory:**
   ```bash
   cd LibraryProject
   ```

2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start Django shell for CRUD operations:**
   ```bash
   python manage.py shell
   ```

4. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## CRUD Operations

Detailed documentation for all CRUD operations can be found in the `docs/` folder:

- **[Complete CRUD Guide](docs/CRUD_operations.md)** - Comprehensive documentation
- **[Create Operations](docs/create.md)** - Creating new books
- **[Retrieve Operations](docs/retrieve.md)** - Reading book data
- **[Update Operations](docs/update.md)** - Modifying existing books
- **[Delete Operations](docs/delete.md)** - Removing books

## Quick Start Example

```python
# In Django shell (python manage.py shell)
from bookshelf.models import Book

# Create a book
book = Book.objects.create(
    title="1984", 
    author="George Orwell", 
    publication_year=1949
)

# Retrieve the book
print(str(book))  # Output: 1984 by George Orwell (1949)

# Update the book
book.title = "Nineteen Eighty-Four"
book.save()

# Delete the book
book.delete()
```

## Technologies Used

- **Django**: Web framework
- **SQLite**: Database (default)
- **Python**: Programming language

## Next Steps

- Implement web views and templates
- Add form handling
- Create admin interface
- Add validation and error handling
- Implement user authentication
