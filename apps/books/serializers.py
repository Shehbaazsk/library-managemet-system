from rest_framework import serializers

from apps.books.models import Book
from apps.users.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Book
        fields = "__all__"


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['is_active', 'is_delete']
