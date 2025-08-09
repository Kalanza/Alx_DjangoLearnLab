from relationship_app.models import Author, Book, Librarian, Library

# Create authors
author1 = Author.objects.create(author="George Orwell")
author2 = Author.objects.create(author="Douglas Adams")
author3 = Author.objects.create(author="Aldous Huxley")

# Create books
book1 = Book.objects.create(title="1984", author=author1)
book2 = Book.objects.create(title="Animal Farm", author=author1)
book3 = Book.objects.create(title="The Hitchhiker's Guide to the Galaxy", author=author2)
book4 = Book.objects.create(title="Brave New World", author=author3)

# Create libraries and add books
library1 = Library.objects.create(name="Kenya National Library")
library1.books.add(book1, book2)

library2 = Library.objects.create(name="Moi University Library")
library2.books.add(book3, book4)

# Create librarians for the libraries
librarian1 = Librarian.objects.create(name="Victor Kalanza", library=library1)
librarian2 = Librarian.objects.create(name="Becky Mwende", library=library2)

# 1. Query all books by a specific author (e.g., George Orwell)
print("Books by George Orwell:")
for book in author1.books.all():
    print(book.title)

# 2. List all books in a library (e.g., Kenya National Library)
library_name = "Kenya National Library"
library = Library.objects.get(name=library_name)
print(f"\nBooks in {library_name}:")
for book in library.books.all():
    print(book.title)

# 3. Retrieve the librarian for a library (e.g., Moi University Library)
print("\nLibrarian for Moi University Library:")
print(library2.librarian.name)