from rest_framework import filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.books.api.service import BookService
from apps.borrow.api.service import BorrowRecordService
from apps.books.models import Book
from apps.books.serializers import BookSerializer, CreateBookSerializer
from apps.borrow.models import BorrowRecord
from apps.borrow.serializers import CreateBorrowRecordSerializer
from apps.utils.logger import get_logger
from apps.utils.permissions import IsAuthorOrAdmin

logger = get_logger(__name__)


class BookBorrowCreateAPIView(CreateAPIView):
    """API for creating books borrow"""
    permission_classes = [AllowAny,]
    serializer_class = CreateBorrowRecordSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            return BorrowRecordService.create_borrow_record(serializer.validated_data)

        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Failed to create book: %s", str(e), exc_info=True)
            return Response({"error": "Failed to create book."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BorrowBookReturnAPIView(APIView):
    permission_classes = [AllowAny,]

    def put(self, request, borrow_record_id):
        """
        Handle PUT request to return a book.
        """
        try:
            return BorrowRecordService.return_book(borrow_record_id)
        except Exception as e:
            logger.error("Failed to create book: %s", str(e), exc_info=True)
            return Response({"error": "Failed to create book."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
