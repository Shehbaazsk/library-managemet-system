from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from apps.books.models import Book
from apps.books.serializers import BookSerializer
from apps.borrow.models import BorrowRecord
from apps.borrow.serializers import BorrowRecordSerializer
from apps.users.models import Author, User
from apps.utils.logger import get_logger

logger = get_logger(__name__)


class BorrowRecordService:

    @staticmethod
    def create_borrow_record(borrow_data):
        """
        Create a new borrow record for the specified book.
        """
        try:
            book = borrow_data.pop('book', None)
            if not book:
                raise ValueError("Book id is required.")
            if book.available_copies > 0:
                borrow_record = BorrowRecord.objects.create(
                    book=book, **borrow_data)
                book.available_copies -= 1
                book.save()
                return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "Book is not available."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            logger.error("Book with id %s does not exist.", book.id)
            return Response(
                {"error": "Book not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except MultipleObjectsReturned:
            logger.error("Multiple books found with id %s.", book.id)
            return Response(
                {"error": "Database integrity error: multiple books found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error("Failed to create borrow record: %s",
                         str(e), exc_info=True)
            return Response({"error": "Failed to create borrow record."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
