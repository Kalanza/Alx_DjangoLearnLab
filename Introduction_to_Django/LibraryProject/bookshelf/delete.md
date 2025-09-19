# Import the model first
from bookshelf.models import Book

# Create the Book instance
book_list = Book(title='1984 ', author='George Orwell', publication_year=1949)

# Save it to the database
book_list.save()

# Verify it was created
print(f"Created book: {book_list.title} by {book_list.author} ({book_list.publication_year})")

# Delete the book
book_list.delete()

# Verify deletion - check if any books remain
remaining_books = Book.objects.all()
print(f"Books remaining in database: {remaining_books.count()}")

for book in remaining_books:
    print(f"Title: {book.title}")
