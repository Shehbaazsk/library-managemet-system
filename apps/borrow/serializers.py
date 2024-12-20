from rest_framework import serializers

from apps.books.serializers import BookSerializer
from apps.borrow.models import BorrowRecord


class ReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['return_date']


class CreateBorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrowed_by']


class BorrowRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BorrowRecord
        fields = ['id', "borrowed_by", "borrow_date", "return_date", "book"]
