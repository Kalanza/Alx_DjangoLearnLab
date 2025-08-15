# CRUD Operations Documentation - Delete

## Deleting Book Data

### Command:
Delete the book you created and confirm the deletion by trying to retrieve all books again.

### Python Commands:

#### 1. First, create a book (if not already created):
```python
from bookshelf.models import Book

>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

#### 2. Delete the book:
```python
>>> book.delete()
(1, {'bookshelf.Book': 1})
```

#### 3. Confirm deletion by retrieving all books:
```python
>>> Book.objects.all()
<QuerySet []>
```

#### 4. Try to retrieve the deleted book (will raise an exception):
```python
>>> Book.objects.get(title="1984")
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "django/db/models/query.py", line 496, in get
    raise self.model.DoesNotExist(
bookshelf.models.Book.DoesNotExist: Book matching query does not exist.
```

### Alternative Delete Methods:

#### Method 1: Delete by ID
```python
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> book_id = book.id
>>> Book.objects.get(id=book_id).delete()
(1, {'bookshelf.Book': 1})

# Verify deletion
>>> Book.objects.filter(id=book_id).exists()
False
```

#### Method 2: Delete using filter and delete()
```python
>>> Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> Book.objects.filter(title="1984").delete()
(1, {'bookshelf.Book': 1})

# Confirm deletion
>>> Book.objects.filter(title="1984").count()
0
```

#### Method 3: Delete multiple books
```python
# Create multiple books
>>> Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> Book.objects.create(title="Animal Farm", author="George Orwell", publication_year=1945)

# Delete all books by George Orwell
>>> Book.objects.filter(author="George Orwell").delete()
(2, {'bookshelf.Book': 2})

# Verify deletion
>>> Book.objects.filter(author="George Orwell").count()
0
```

#### Method 4: Delete all books
```python
>>> Book.objects.all().delete()
(0, {})  # If no books exist, or (n, {'bookshelf.Book': n}) if n books deleted
```

### Complete Delete Example:
```python
# Create a book
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
>>> print(f"Created: {str(book)}")
Created: 1984 by George Orwell (1949)

# Check total books before deletion
>>> print(f"Total books before deletion: {Book.objects.count()}")
Total books before deletion: 1

# Delete the book
>>> deletion_result = book.delete()
>>> print(f"Deletion result: {deletion_result}")
Deletion result: (1, {'bookshelf.Book': 1})

# Confirm deletion
>>> print(f"Total books after deletion: {Book.objects.count()}")
Total books after deletion: 0

>>> print(f"All books: {Book.objects.all()}")
All books: <QuerySet []>
```

### Expected Output:

#### For book.delete():
```python
(1, {'bookshelf.Book': 1})
# Format: (number_of_objects_deleted, {'model_name': count})
```

#### For Book.objects.all() after deletion:
```python
<QuerySet []>  # Empty QuerySet
```

#### For attempting to retrieve deleted book:
```python
bookshelf.models.Book.DoesNotExist: Book matching query does not exist.
```

#### For checking if book exists:
```python
>>> Book.objects.filter(title="1984").exists()
False
```

### Verification Methods:

#### 1. Using count():
```python
>>> Book.objects.count()
0
```

#### 2. Using exists():
```python
>>> Book.objects.filter(title="1984").exists()
False
```

#### 3. Using all():
```python
>>> Book.objects.all()
<QuerySet []>
```

#### 4. Try to get specific book (will raise exception):
```python
>>> Book.objects.get(title="1984")
# Raises: bookshelf.models.Book.DoesNotExist
```

### Key Points:

1. **Return Value**: `delete()` returns a tuple `(number_deleted, details_dict)`
2. **Instance vs QuerySet**: 
   - `instance.delete()` deletes one object
   - `QuerySet.delete()` can delete multiple objects
3. **Permanent Action**: Deletion is permanent and cannot be undone
4. **Cascade Effects**: Related objects may also be deleted based on foreign key relationships
5. **Verification**: Always verify deletion using `count()`, `exists()`, or `all()`

### Notes:
- Use `exists()` instead of `count()` for better performance when checking if records exist
- The `delete()` method returns useful information about what was deleted
- Always be careful with bulk delete operations
- Consider using soft deletes for important data that might need recovery