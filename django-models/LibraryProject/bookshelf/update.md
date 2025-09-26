# Import the modefor book in books:
     print(f"Title: {book.title}")first
from bookshelf.models import Book

# Create the Book instance
book_list = Book(title='1984 ', author='George Orwell', publication_year=1949)

# Save it to the database
book_list.save()

# Verify it was created

book_list.title = "Nineteen Eighty-Four"

book_list.save()

books = Book.objects.all()

for book in books:
     print(f"Title :{book.title})"