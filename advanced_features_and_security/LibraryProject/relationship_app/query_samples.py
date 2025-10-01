from relationship_app.models import Author, Book, Library, Librarian

#Query all books by a specific author
# First get a specific author, then get their books
author = Author.objects.get(name=author_name)  # Replace with actual author name
books_by_author_filter = Book.objects.filter(author=author)

#List all books in a library
# First get a specific library, then get their books
library = Library.objects.get(name=library_name)  # Replace with actual library name
books_in_library = library.books.all()

#Retrieve Librarian for a library 
# Get the librarian associated with a specific library
librarian = Librarian.objects.get(library=library)
