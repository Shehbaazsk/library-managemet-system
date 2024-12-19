from rest_framework import serializers

from apps.borrow.models import BorrowRecord


class ReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['return_date']


class CreateBorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrowed_by', 'borrow_date']
