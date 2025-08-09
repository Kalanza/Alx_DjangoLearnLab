# CRUD Operations Documentation - Complete Guide

## Overview
This document demonstrates all CRUD (Create, Read, Update, Delete) operations for the Book model in the Django bookshelf application.

## Book Model Definition
```python
# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
```

## Complete CRUD Operations Sequence

### Prerequisites
```python
# Start Django shell
# python manage.py shell

from bookshelf.models import Book
```

---

## 1. CREATE Operation

### Command:
Create a Book instance with the title "1984", author "George Orwell", and publication year 1949.

### Implementation:
```python
>>> from bookshelf.models import Book
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> book.title
'1984'
>>> book.author
'George Orwell'
>>> book.publication_year
1949
>>> book.id
1
>>> str(book)
'1984 by George Orwell (1949)'
```

### Expected Output:
- **Successful Creation**: Book instance created with ID 1
- **Title**: `'1984'`
- **Author**: `'George Orwell'`
- **Publication Year**: `1949`
- **String Representation**: `'1984 by George Orwell (1949)'`

**📋 Detailed Documentation**: See [create.md](create.md)

---

## 2. RETRIEVE Operation

### Command:
Retrieve and display all attributes of the book you just created.

### Implementation:
```python
>>> book = Book.objects.get(id=1)
>>> str(book)
'1984 by George Orwell (1949)'
>>> book.title
'1984'
>>> book.author
'George Orwell'
>>> book.publication_year
1949

# Retrieve all books
>>> Book.objects.all()
<QuerySet [<Book: 1984 by George Orwell (1949)>]>

# Count total books
>>> Book.objects.count()
1
```

### Expected Output:
- **String Representation**: `'1984 by George Orwell (1949)'`
- **All Books Query**: `<QuerySet [<Book: 1984 by George Orwell (1949)>]>`
- **Total Count**: `1`

**📋 Detailed Documentation**: See [retrieve.md](retrieve.md)

---

## 3. UPDATE Operation

### Command:
Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

### Implementation:
```python
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> str(book)
'Nineteen Eighty-Four by George Orwell (1949)'

# Verify the update persisted
>>> updated_book = Book.objects.get(id=1)
>>> updated_book.title
'Nineteen Eighty-Four'
```

### Expected Output:
- **Updated String Representation**: `'Nineteen Eighty-Four by George Orwell (1949)'`
- **Updated Title**: `'Nineteen Eighty-Four'`
- **Other Fields Unchanged**: Author and publication year remain the same

**📋 Detailed Documentation**: See [update.md](update.md)

---

## 4. DELETE Operation

### Command:
Delete the book you created and confirm the deletion by trying to retrieve all books again.

### Implementation:
```python
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})

# Confirm deletion
>>> Book.objects.all()
<QuerySet []>

>>> Book.objects.count()
0

# Try to retrieve the deleted book (will raise exception)
>>> Book.objects.get(title="Nineteen Eighty-Four")
Traceback (most recent call last):
  ...
bookshelf.models.Book.DoesNotExist: Book matching query does not exist.
```

### Expected Output:
- **Deletion Result**: `(1, {'bookshelf.Book': 1})` - 1 object deleted
- **Empty QuerySet**: `<QuerySet []>`
- **Zero Count**: `0`
- **Exception on Retrieval**: `Book.DoesNotExist` exception

**📋 Detailed Documentation**: See [delete.md](delete.md)

---

## Complete CRUD Workflow Example

```python
# Complete workflow in one session
from bookshelf.models import Book

# CREATE
print("=== CREATE ===")
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Created: {str(book)}")
print(f"Total books: {Book.objects.count()}")

# RETRIEVE
print("\n=== RETRIEVE ===")
retrieved_book = Book.objects.get(id=book.id)
print(f"Retrieved: {str(retrieved_book)}")
print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Year: {retrieved_book.publication_year}")

# UPDATE
print("\n=== UPDATE ===")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated: {str(book)}")

# DELETE
print("\n=== DELETE ===")
deletion_result = book.delete()
print(f"Deletion result: {deletion_result}")
print(f"Total books after deletion: {Book.objects.count()}")
print(f"All books: {Book.objects.all()}")
```

### Expected Complete Output:
```
=== CREATE ===
Created: 1984 by George Orwell (1949)
Total books: 1

=== RETRIEVE ===
Retrieved: 1984 by George Orwell (1949)
Title: 1984
Author: George Orwell
Year: 1949

=== UPDATE ===
Updated: Nineteen Eighty-Four by George Orwell (1949)

=== DELETE ===
Deletion result: (1, {'bookshelf.Book': 1})
Total books after deletion: 0
All books: <QuerySet []>
```

---

## Summary

| Operation | Command | Result |
|-----------|---------|---------|
| **Create** | `Book.objects.create(...)` | New Book instance with ID |
| **Retrieve** | `Book.objects.get(...)` | Book instance or QuerySet |
| **Update** | `book.field = value; book.save()` | Modified Book instance |
| **Delete** | `book.delete()` | Deletion confirmation tuple |

## Key Django ORM Methods Used

- `objects.create()` - Create and save new instance
- `objects.get()` - Retrieve single instance
- `objects.all()` - Retrieve all instances
- `objects.filter()` - Retrieve filtered instances
- `objects.count()` - Count instances
- `save()` - Save changes to existing instance
- `delete()` - Delete instance(s)

## Files Structure
```
LibraryProject/
├── manage.py               # Django management script
├── LibraryProject/        # Main project settings
├── bookshelf/             # Django app
│   ├── models.py          # Book model definition
│   └── ...               # Other app files
└── docs/                  # Documentation
    ├── CRUD_operations.md # This comprehensive guide
    ├── create.md          # CREATE operation details
    ├── retrieve.md        # RETRIEVE operation details
    ├── update.md          # UPDATE operation details
    └── delete.md          # DELETE operation details
```

## Next Steps
1. Test these operations in Django shell: `python manage.py shell`
2. Explore more complex queries and relationships
3. Implement views and forms for web interface
4. Add validation and error handling