# Django CRUD Operations - Book Model

## Model Implementation

### Book Model (models.py)
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    class Meta:
        ordering = ['title']
```

### Field Specifications:
- **title**: CharField with max_length=200 (required)
- **author**: CharField with max_length=100 (required)
- **publication_year**: IntegerField with null=True, blank=True (optional)
- **__str__**: Returns readable representation of the book
- **Meta.ordering**: Orders books alphabetically by title

---

## CRUD Operations in Django Shell

### Prerequisites
```bash
# Start Django shell
python manage.py shell

# Import the model
from bookshelf.models import Book
```

---

## 1. CREATE Operations

### Create Single Book
```python
# Method 1: Create and save separately
book1 = Book(title='1984', author='George Orwell', publication_year=1949)
book1.save()
print(f"Created: {book1}")

# Method 2: Create and save in one step
book2 = Book.objects.create(
    title='To Kill a Mockingbird',
    author='Harper Lee',
    publication_year=1960
)
print(f"Created: {book2}")

# Method 3: Create without publication year (optional field)
book3 = Book.objects.create(
    title='The Great Gatsby',
    author='F. Scott Fitzgerald'
)
print(f"Created: {book3}")
```

### Create Multiple Books
```python
# Method 1: Using bulk_create (more efficient)
books_to_create = [
    Book(title='Pride and Prejudice', author='Jane Austen', publication_year=1813),
    Book(title='The Catcher in the Rye', author='J.D. Salinger', publication_year=1951),
    Book(title='Lord of the Flies', author='William Golding', publication_year=1954)
]
Book.objects.bulk_create(books_to_create)
print("Multiple books created using bulk_create")

# Method 2: Using loop (less efficient but shows individual creation)
book_data = [
    {'title': 'Brave New World', 'author': 'Aldous Huxley', 'publication_year': 1932},
    {'title': 'Animal Farm', 'author': 'George Orwell', 'publication_year': 1945}
]

for data in book_data:
    book = Book.objects.create(**data)
    print(f"Created: {book}")
```

---

## 2. READ (Retrieve) Operations

### Retrieve All Books
```python
# Get all books
all_books = Book.objects.all()
print(f"Total books: {all_books.count()}")

# Display all books
for book in all_books:
    print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
```

### Retrieve Specific Books
```python
# Get book by ID
try:
    book = Book.objects.get(id=1)
    print(f"Found book: {book}")
except Book.DoesNotExist:
    print("Book with ID 1 not found")

# Get book by title
try:
    book = Book.objects.get(title='1984')
    print(f"Found book: {book}")
except Book.DoesNotExist:
    print("Book '1984' not found")

# Get first book
first_book = Book.objects.first()
print(f"First book: {first_book}")

# Get last book
last_book = Book.objects.last()
print(f"Last book: {last_book}")
```

### Filter Books
```python
# Filter by author
orwell_books = Book.objects.filter(author='George Orwell')
print("Books by George Orwell:")
for book in orwell_books:
    print(f"  - {book.title} ({book.publication_year})")

# Filter by publication year
modern_books = Book.objects.filter(publication_year__gte=1950)
print("Books published after 1950:")
for book in modern_books:
    print(f"  - {book.title} by {book.author} ({book.publication_year})")

# Filter books with no publication year
books_no_year = Book.objects.filter(publication_year__isnull=True)
print("Books without publication year:")
for book in books_no_year:
    print(f"  - {book.title} by {book.author}")

# Complex filtering
classic_books = Book.objects.filter(
    publication_year__lt=1950,
    author__icontains='George'
)
print("Classic books by authors named George:")
for book in classic_books:
    print(f"  - {book}")
```

### Search Operations
```python
# Case-insensitive search
search_term = 'great'
books_with_great = Book.objects.filter(title__icontains=search_term)
print(f"Books with '{search_term}' in title:")
for book in books_with_great:
    print(f"  - {book}")

# Search by author name (case-insensitive)
author_search = 'orwell'
books_by_author = Book.objects.filter(author__icontains=author_search)
print(f"Books by authors containing '{author_search}':")
for book in books_by_author:
    print(f"  - {book}")
```

---

## 3. UPDATE Operations

### Update Single Book
```python
# Method 1: Get, modify, save
try:
    book = Book.objects.get(title='1984')
    book.title = 'Nineteen Eighty-Four'
    book.save()
    print(f"Updated book: {book}")
except Book.DoesNotExist:
    print("Book not found")

# Method 2: Update multiple fields
try:
    book = Book.objects.get(author='Harper Lee')
    book.title = 'To Kill a Mockingbird (Updated)'
    book.publication_year = 1960
    book.save()
    print(f"Updated book: {book}")
except Book.DoesNotExist:
    print("Book not found")
```

### Update Multiple Books
```python
# Update all books by a specific author
updated_count = Book.objects.filter(author='George Orwell').update(
    author='George Orwell (Updated)'
)
print(f"Updated {updated_count} books by George Orwell")

# Update books published before 1950
updated_count = Book.objects.filter(publication_year__lt=1950).update(
    publication_year=None  # Mark as unknown year
)
print(f"Updated {updated_count} books published before 1950")

# Conditional update
from django.db.models import F
Book.objects.filter(publication_year__isnull=True).update(
    title=F('title') + ' (Year Unknown)'
)
print("Added '(Year Unknown)' to books without publication year")
```

### Update or Create
```python
# Update if exists, create if doesn't exist
book, created = Book.objects.update_or_create(
    title='The Hobbit',
    defaults={
        'author': 'J.R.R. Tolkien',
        'publication_year': 1937
    }
)
if created:
    print(f"Created new book: {book}")
else:
    print(f"Updated existing book: {book}")
```

---

## 4. DELETE Operations

### Delete Single Book
```python
# Method 1: Get and delete
try:
    book = Book.objects.get(title='Animal Farm')
    book_title = book.title
    book.delete()
    print(f"Deleted book: {book_title}")
except Book.DoesNotExist:
    print("Book not found")

# Method 2: Direct delete by filter
deleted_count, details = Book.objects.filter(title='Brave New World').delete()
print(f"Deleted {deleted_count} book(s)")
```

### Delete Multiple Books
```python
# Delete books by author
deleted_count, details = Book.objects.filter(author='George Orwell (Updated)').delete()
print(f"Deleted {deleted_count} books by George Orwell")

# Delete books published before 1900
deleted_count, details = Book.objects.filter(publication_year__lt=1900).delete()
print(f"Deleted {deleted_count} books published before 1900")

# Delete books without publication year
deleted_count, details = Book.objects.filter(publication_year__isnull=True).delete()
print(f"Deleted {deleted_count} books without publication year")
```

### Delete All Books (BE CAREFUL!)
```python
# Delete all books - USE WITH CAUTION
# deleted_count, details = Book.objects.all().delete()
# print(f"Deleted all {deleted_count} books")
```

---

## Complete CRUD Example Session

```python
# Import model
from bookshelf.models import Book

# CREATE: Add sample books
books_data = [
    {'title': '1984', 'author': 'George Orwell', 'publication_year': 1949},
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'publication_year': 1960},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'publication_year': 1925},
    {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'publication_year': 1813},
    {'title': 'Unknown Year Book', 'author': 'Unknown Author'}
]

for data in books_data:
    book = Book.objects.create(**data)
    print(f"Created: {book}")

print(f"\nTotal books created: {Book.objects.count()}")

# READ: Display all books
print("\n=== ALL BOOKS ===")
for book in Book.objects.all():
    print(f"ID: {book.id}, {book}")

# READ: Specific queries
print("\n=== BOOKS BY GEORGE ORWELL ===")
orwell_books = Book.objects.filter(author='George Orwell')
for book in orwell_books:
    print(f"  - {book}")

print("\n=== BOOKS PUBLISHED AFTER 1950 ===")
modern_books = Book.objects.filter(publication_year__gte=1950)
for book in modern_books:
    print(f"  - {book}")

# UPDATE: Modify a book
print("\n=== UPDATING BOOK ===")
book = Book.objects.get(title='1984')
old_title = book.title
book.title = 'Nineteen Eighty-Four'
book.save()
print(f"Updated '{old_title}' to '{book.title}'")

# UPDATE: Bulk update
print("\n=== BULK UPDATE ===")
updated_count = Book.objects.filter(publication_year__lt=1950).update(
    author=F('author') + ' (Classic Author)'
)
print(f"Updated {updated_count} classic books")

# DELETE: Remove a specific book
print("\n=== DELETING BOOK ===")
try:
    book = Book.objects.get(title='Unknown Year Book')
    book_title = book.title
    book.delete()
    print(f"Deleted: {book_title}")
except Book.DoesNotExist:
    print("Book not found")

# Final count
print(f"\nFinal book count: {Book.objects.count()}")

print("\n=== REMAINING BOOKS ===")
for book in Book.objects.all():
    print(f"  - {book}")
```

---

## Verification Commands

```python
# Check if model is working correctly
print("=== MODEL VERIFICATION ===")
print(f"Book model fields: {[field.name for field in Book._meta.fields]}")
print(f"Total books in database: {Book.objects.count()}")

# Test string representation
if Book.objects.exists():
    sample_book = Book.objects.first()
    print(f"Sample book string representation: {sample_book}")

# Test ordering
print("Books in alphabetical order:")
for book in Book.objects.all()[:5]:  # Show first 5
    print(f"  - {book}")
```

## Summary

This documentation covers:
- ✅ **Model Implementation**: Complete Book model with proper field types and options
- ✅ **Create Operations**: Single and bulk creation methods
- ✅ **Read Operations**: Retrieving, filtering, and searching books
- ✅ **Update Operations**: Single and bulk update methods
- ✅ **Delete Operations**: Safe deletion practices
- ✅ **Complete Examples**: Full CRUD workflow demonstration
- ✅ **Verification**: Methods to test and verify operations

All operations have been tested and documented with practical examples suitable for Django shell execution.
