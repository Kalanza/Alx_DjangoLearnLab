# CRUD Operations Documentation - Update

## Updating Book Data

### Command:
Update the title of "1984" to "Nineteen Eighty-Four" and save the changes.

### Python Commands:

#### 1. First, create a book (if not already created):
```python
from bookshelf.models import Book

>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

#### 2. Update the title and save the changes:
```python
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> str(book)
'Nineteen Eighty-Four by George Orwell (1949)'
```

#### 3. Verify the update by retrieving the book again:
```python
>>> updated_book = Book.objects.get(id=book.id)
>>> updated_book.title
'Nineteen Eighty-Four'

>>> str(updated_book)
'Nineteen Eighty-Four by George Orwell (1949)'
```

### Alternative Update Methods:

#### Method 1: Update individual fields
```python
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.author = "George Orwell"  # Can update multiple fields
>>> book.publication_year = 1949
>>> book.save()
>>> str(book)
'Nineteen Eighty-Four by George Orwell (1949)'
```

#### Method 2: Using update() method for single record
```python
>>> Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")
1  # Returns number of records updated

>>> book = Book.objects.get(author="George Orwell")
>>> str(book)
'Nineteen Eighty-Four by George Orwell (1949)'
```

#### Method 3: Update multiple fields at once using update()
```python
>>> Book.objects.filter(author="George Orwell").update(
...     title="Nineteen Eighty-Four",
...     publication_year=1949
... )
1  # Returns number of records updated
```

#### Method 4: Get, modify, and save pattern
```python
>>> book = Book.objects.get(id=1)
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()

# Verify the change
>>> Book.objects.get(id=1).title
'Nineteen Eighty-Four'
```

### Expected Output:

#### After updating title:
```python
>>> str(book)
'Nineteen Eighty-Four by George Orwell (1949)'
```

#### After using update() method:
```python
>>> Book.objects.filter(title="1984").update(title="Nineteen Eighty-Four")
1  # Number of records updated
```

#### Verification of update:
```python
>>> book.title
'Nineteen Eighty-Four'
```

### Complete Update Example:
```python
# Start with original book
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> print(f"Original: {str(book)}")
Original: 1984 by George Orwell (1949)

# Update the title
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> print(f"Updated: {str(book)}")
Updated: Nineteen Eighty-Four by George Orwell (1949)

# Verify persistence by fetching from database
>>> fresh_book = Book.objects.get(id=book.id)
>>> print(f"From DB: {str(fresh_book)}")
From DB: Nineteen Eighty-Four by George Orwell (1949)
```

### Key Differences Between Update Methods:

1. **Instance.save()**: 
   - Works on individual model instances
   - Calls the model's `save()` method (triggers signals)
   - Updates all fields of the instance

2. **QuerySet.update()**:
   - Works on QuerySets (can update multiple records)
   - More efficient for bulk updates
   - Does NOT call `save()` method or trigger signals
   - Returns number of affected rows

### Notes:
- Always call `save()` after modifying instance attributes
- The `update()` method is more efficient for bulk operations
- Changes are not persisted until `save()` is called (for instance method)
- Use `refresh_from_db()` to reload an instance from the database if needed