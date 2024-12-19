from rest_framework import filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.books.api.service import BookService
from apps.books.models import Book
from apps.books.serializers import BookSerializer, CreateBookSerializer
from apps.utils.logger import get_logger
from apps.utils.permissions import IsAuthorOrAdmin

logger = get_logger(__name__)


class BookListCreateAPIView(ListCreateAPIView):
    """API for listing and creating books"""
    permission_classes = [AllowAny,]
    queryset = Book.objects.select_related('author').all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'isbn', 'author__first_name',]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookSerializer
        elif self.request.method == 'POST':
            return CreateBookSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            if self.request.user and self.request.user.is_authenticated:
                return [IsAuthenticated()]
            elif self.request.user and self.request.user.is_admin:
                return [IsAdminUser()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = request.user
            book_data = serializer.validated_data

            return BookService.create_book(user, book_data)

        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Failed to create book: %s", str(e), exc_info=True)
            return Response({"error": "Failed to create book."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# HERE WE CAN ALSO CUSTOMIZE LIKE WE DID IN LIST AND CREATE
class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """API for retrieving, updating, and deleting a book"""
    permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
    queryset = Book.objects.select_related('author').all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return CreateBookSerializer
        return BookSerializer
