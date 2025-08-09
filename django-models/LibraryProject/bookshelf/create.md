# CRUD Operations Documentation - Create

## Creating a Book Instance

### Command:
Create a Book instance with the title "1984", author "George Orwell", and publication year 1949.

### Python Commands:
```python
from bookshelf.models import Book

# Create a new Book instance
>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Verify the book was created by accessing its attributes
>>> book.title
'1984'

>>> book.author
'George Orwell'

>>> book.publication_year
1949

# Display the string representation of the book
>>> str(book)
'1984 by George Orwell (1949)'

# Check the book's ID (primary key)
>>> book.id
1
```

### Expected Output:
- **Successful Creation**: The `Book.objects.create()` method returns a Book instance object
- **Title Access**: `book.title` returns `'1984'`
- **Author Access**: `book.author` returns `'George Orwell'`
- **Publication Year Access**: `book.publication_year` returns `1949`
- **String Representation**: `str(book)` returns `'1984 by George Orwell (1949)'`
- **Primary Key**: `book.id` returns `1` (or the next available integer if other books exist)

### Alternative Creation Method:
```python
# Alternative way to create a book instance
>>> book = Book(title="1984", author="George Orwell", publication_year=1949)
>>> book.save()  # Don't forget to save when using this method

# Verify creation
>>> book.id  # Will show the assigned ID after save()
1
```

### Notes:
- The `create()` method automatically saves the instance to the database
- The alternative method using `Book()` requires calling `.save()` manually
- The `__str__` method in the model provides a readable string representation
- Each book gets a unique `id` (primary key) automatically assigned by Django