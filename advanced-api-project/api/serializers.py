from rest_framework import serializers
from datetime import date
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model with custom validation.
    
    This serializer handles the serialization and deserialization of Book instances.
    It includes custom validation to ensure that the publication year is not in the future.
    
    Fields:
        - All fields from the Book model (title, publication_year, author)
        
    Custom Validation:
        - publication_year: Ensures the year is not greater than the current year
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested book serialization.
    
    This serializer includes the author's basic information along with a nested
    representation of all books written by the author. The books are serialized
    using the BookSerializer, creating a dynamic nested relationship.
    
    Fields:
        - name: Author's name
        - books: Nested serialization of all books by this author (read-only)
        
    Relationship Handling:
        The 'books' field uses the related_name='books' defined in the Book model's
        foreign key relationship. This allows automatic fetching and serialization
        of all books associated with an author.
    """
    
    # Nested serialization of related books
    # Using 'many=True' because one author can have multiple books
    # 'read_only=True' because we don't want to create/update books through author serializer
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
