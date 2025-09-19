# Import the model first
from bookshelf.models import Book

# Method 1: Create and save in one step
book_list = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)

# Verify it was created (no need to call save() - already saved)
print(f"Created book: {book_list.title} by {book_list.author} ({book_list.publication_year})")

