# Advanced API Project - Django REST Framework

## Project Overview

This Django project demonstrates advanced API development with Django REST Framework, focusing on custom serializers that handle complex data structures and nested relationships.

## Features

- **Custom Models**: Author and Book models with proper relationships
- **Custom Serializers**: Advanced serializers with nested data and custom validation
- **Data Validation**: Custom validation to prevent future publication years
- **Nested Relationships**: Authors serialized with their related books
- **Django Admin Integration**: Full admin interface for easy testing

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py      # Django settings with DRF configuration
│   ├── urls.py          # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py        # Author and Book models
│   ├── serializers.py   # Custom serializers with validation
│   ├── views.py         # API views
│   ├── admin.py         # Django admin configuration
│   └── urls.py          # API URL patterns
├── manage.py
├── db.sqlite3
└── test_models_serializers.py  # Test script
```

## Models

### Author Model
- `name`: CharField - Author's full name
- Establishes one-to-many relationship with Book model

### Book Model
- `title`: CharField - Book title
- `publication_year`: IntegerField - Publication year
- `author`: ForeignKey - Reference to Author model
- Includes unique constraint to prevent duplicate books by same author

## Serializers

### BookSerializer
- Serializes all Book model fields
- **Custom Validation**: Ensures `publication_year` is not in the future
- Provides detailed error messages for validation failures

### AuthorSerializer
- Serializes Author model with nested book data
- **Nested Relationship**: Dynamically includes all books by the author
- Uses `BookSerializer` for nested book serialization
- Read-only nested books to prevent unintended modifications

## API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/authors/` | GET | List all authors with nested books |
| `/api/authors/` | POST | Create new author |
| `/api/authors/<id>/` | GET | Retrieve specific author with books |
| `/api/authors/<id>/` | PUT/PATCH | Update author |
| `/api/authors/<id>/` | DELETE | Delete author |
| `/api/books/` | GET | List all books |
| `/api/books/` | POST | Create new book (with validation) |
| `/api/books/<id>/` | GET | Retrieve specific book |
| `/api/books/<id>/` | PUT/PATCH | Update book (with validation) |
| `/api/books/<id>/` | DELETE | Delete book |

## Setup Instructions

### 1. Install Dependencies
```bash
pip install django djangorestframework
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/api/`
Django Admin: `http://127.0.0.1:8000/admin/`

## Testing

### Manual Testing via Django Shell
Run the test script:
```bash
python manage.py shell -c "exec(open('test_models_serializers.py').read())"
```

### Test Cases Covered
1. **Model Creation**: Creating Author and Book instances
2. **Serialization**: Testing BookSerializer and AuthorSerializer
3. **Nested Relationships**: Verifying authors include their books
4. **Custom Validation**: Testing future year validation (should fail)
5. **Valid Data**: Testing successful book creation through serializer

## Key Implementation Details

### Relationship Handling
- **Foreign Key**: Book model has `author` field with `CASCADE` delete
- **Related Name**: Uses `related_name='books'` for reverse lookup
- **Nested Serialization**: AuthorSerializer includes books via `BookSerializer(many=True, read_only=True)`

### Custom Validation
- **Publication Year**: Validates against current year using `date.today().year`
- **Error Messages**: Provides clear, user-friendly validation messages
- **Serializer Method**: Uses `validate_publication_year()` method

### Django REST Framework Configuration
- Added `rest_framework` to `INSTALLED_APPS`
- Uses generic views for standard CRUD operations
- Implements proper HTTP methods (GET, POST, PUT, PATCH, DELETE)

## Example Usage

### Creating an Author with Books
```json
POST /api/authors/
{
    "name": "J.K. Rowling"
}

POST /api/books/
{
    "title": "Harry Potter and the Philosopher's Stone",
    "publication_year": 1997,
    "author": 1
}
```

### Retrieving Author with Nested Books
```json
GET /api/authors/1/
{
    "id": 1,
    "name": "J.K. Rowling",
    "books": [
        {
            "id": 1,
            "title": "Harry Potter and the Philosopher's Stone",
            "publication_year": 1997,
            "author": 1
        }
    ]
}
```

### Validation Error Example
```json
POST /api/books/
{
    "title": "Future Book",
    "publication_year": 2026,
    "author": 1
}

Response (400 Bad Request):
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2025."
    ]
}
```

## Development Notes

- Uses SQLite database for simplicity
- Includes comprehensive docstrings and comments
- Follows Django and DRF best practices
- Implements proper error handling and validation
- Provides detailed API documentation

This project serves as a foundation for building more complex APIs with Django REST Framework, demonstrating proper use of custom serializers, nested relationships, and data validation.
