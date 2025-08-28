"""
Test script for models and serializers.

This script demonstrates creating, retrieving, and serializing Author and Book instances
to verify that our models and serializers work as expected.
"""

# Test the models and serializers
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from datetime import date

# Create test authors
print("=== Creating Authors ===")
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")
print(f"Created authors: {author1}, {author2}")

# Create test books
print("\n=== Creating Books ===")
book1 = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone", 
    publication_year=1997, 
    author=author1
)
book2 = Book.objects.create(
    title="Harry Potter and the Chamber of Secrets", 
    publication_year=1998, 
    author=author1
)
book3 = Book.objects.create(
    title="1984", 
    publication_year=1949, 
    author=author2
)
print(f"Created books: {book1}, {book2}, {book3}")

# Test BookSerializer
print("\n=== Testing BookSerializer ===")
book_serializer = BookSerializer(book1)
print("Book serialized data:")
print(book_serializer.data)

# Test AuthorSerializer with nested books
print("\n=== Testing AuthorSerializer with nested books ===")
author_serializer = AuthorSerializer(author1)
print("Author with nested books:")
print(author_serializer.data)

# Test custom validation (should fail for future year)
print("\n=== Testing Custom Validation (Future Year) ===")
try:
    invalid_book_data = {
        'title': 'Future Book',
        'publication_year': date.today().year + 1,
        'author': author1.id
    }
    invalid_serializer = BookSerializer(data=invalid_book_data)
    if not invalid_serializer.is_valid():
        print("Validation failed as expected:")
        print(invalid_serializer.errors)
    else:
        print("ERROR: Validation should have failed!")
except Exception as e:
    print(f"Exception occurred: {e}")

# Test valid book creation through serializer
print("\n=== Testing Valid Book Creation ===")
valid_book_data = {
    'title': 'Animal Farm',
    'publication_year': 1945,
    'author': author2.id
}
valid_serializer = BookSerializer(data=valid_book_data)
if valid_serializer.is_valid():
    new_book = valid_serializer.save()
    print(f"Successfully created book: {new_book}")
else:
    print("Validation failed:")
    print(valid_serializer.errors)

print("\n=== Test completed successfully! ===")
