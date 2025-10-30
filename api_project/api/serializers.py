from models import Book
from rest_framework import serializers
class BookSerializer(serializers.ModelSerializer):
    serializer = Book.object.all()
    fields = '__all__'