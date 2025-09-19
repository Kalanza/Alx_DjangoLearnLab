# Import the model first
from bookshelf.models import Book

# Create the Book instance
book_list = Book.objects.create(title='1984 ', author='George Orwell', publication_year=1949)

# Verify it was created
print(f"Created book: {book_list.title} by {book_list.author} ({book_list.publication_year})")

book1 = Book(title='1984 ', author='George Orwell', publication_year=1949)

#Retrieve Command
all_books = Book.objects.get()

for books in all_books:
   print(f"Title = {books.title}, Author: {books.author}, Year: {books.publication_year}")