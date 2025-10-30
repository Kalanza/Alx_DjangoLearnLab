from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
# Create your views here.
class BookList(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()