# CRUD Operations Documentation - Retrieve

## Retrieving Book Data

### Command:
Retrieve and display all attributes of the book you just created.

### Python Commands:

#### 1. First, create a book (if not already created):
```python
from bookshelf.models import Book

>>> book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```

#### 2. Retrieve and display the book using string representation:
```python
>>> str(book)
'1984 by George Orwell (1949)'
```

#### 3. Retrieve individual attributes:
```python
>>> book.id
1

>>> book.title
'1984'

>>> book.author
'George Orwell'

>>> book.publication_year
1949
```

#### 4. Retrieve all books from the database:
```python
>>> all_books = Book.objects.all()
>>> all_books
<QuerySet [<Book: 1984 by George Orwell (1949)>]>

>>> for book in all_books:
...     print(book)
1984 by George Orwell (1949)
```

#### 5. Retrieve a specific book by ID:
```python
>>> book_by_id = Book.objects.get(id=1)
>>> book_by_id
<Book: 1984 by George Orwell (1949)>

>>> str(book_by_id)
'1984 by George Orwell (1949)'
```

#### 6. Retrieve a book by title:
```python
>>> book_by_title = Book.objects.get(title="1984")
>>> book_by_title.author
'George Orwell'

>>> book_by_title.publication_year
1949
```

#### 7. Filter books by author:
```python
>>> orwell_books = Book.objects.filter(author="George Orwell")
>>> orwell_books
<QuerySet [<Book: 1984 by George Orwell (1949)>]>

>>> for book in orwell_books:
...     print(f"Title: {book.title}, Year: {book.publication_year}")
Title: 1984, Year: 1949
```

#### 8. Display all attributes in a formatted way:
```python
>>> book = Book.objects.get(title="1984")
>>> print(f"ID: {book.id}")
>>> print(f"Title: {book.title}")
>>> print(f"Author: {book.author}")
>>> print(f"Publication Year: {book.publication_year}")
>>> print(f"String Representation: {str(book)}")
```

### Expected Output:

#### For string representation:
```
'1984 by George Orwell (1949)'
```

#### For individual attributes:
- **ID**: `1`
- **Title**: `'1984'`
- **Author**: `'George Orwell'`
- **Publication Year**: `1949`

#### For all books query:
```
<QuerySet [<Book: 1984 by George Orwell (1949)>]>
```

#### For formatted display:
```
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
String Representation: 1984 by George Orwell (1949)
```

### Common Retrieve Methods:

1. **`objects.all()`** - Retrieves all book instances
2. **`objects.get()`** - Retrieves a single book (raises exception if not found or multiple found)
3. **`objects.filter()`** - Retrieves books matching specified criteria
4. **`objects.first()`** - Retrieves the first book in the queryset
5. **`objects.last()`** - Retrieves the last book in the queryset

### Notes:
- Use `get()` when you expect exactly one result
- Use `filter()` when you might get multiple results or zero results
- `get()` raises `DoesNotExist` exception if no book is found
- `get()` raises `MultipleObjectsReturned` exception if multiple books match
- QuerySets are lazy and only execute when evaluated (e.g., when iterating or converting to list)