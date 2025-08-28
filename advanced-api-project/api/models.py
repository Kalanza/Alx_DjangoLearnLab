from django.db import models


class Author(models.Model):
    """
    Author model representing book authors.
    
    This model stores basic information about authors and establishes
    a one-to-many relationship with the Book model (one author can have
    multiple books).
    
    Fields:
        name: The author's full name
    """
    name = models.CharField(max_length=100, help_text="Author's full name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing individual books.
    
    This model stores information about books and links to the Author model
    through a foreign key relationship. Each book belongs to one author,
    but an author can have multiple books.
    
    Fields:
        title: The book's title
        publication_year: The year the book was published
        author: Foreign key reference to the Author model
    """
    title = models.CharField(max_length=200, help_text="Book title")
    publication_year = models.IntegerField(help_text="Year the book was published")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="Author of the book"
    )
    
    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        ordering = ['title']
        unique_together = ['title', 'author']  # Prevent duplicate books by same author
