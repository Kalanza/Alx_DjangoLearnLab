from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    List all books. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides CRUD operations: create, retrieve, update, delete.
    Requires authentication for all operations.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
