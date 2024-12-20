from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.books.models import Book
from apps.books.serializers import BookSerializer
from apps.users.models import Author, User
from apps.utils.logger import get_logger

logger = get_logger(__name__)


class BookService:

    @staticmethod
    def create_book(user, book_data):
        """
        Create a new book for the specified user.
        If the user is an admin, they can specify the author.
        If the user is an authenticated author, they can only create books for themselves.
        """
        try:
            if user.is_superuser:
                user_id = book_data.get('author')
                if not user_id:
                    raise PermissionDenied(
                        "An author must be specified for this book.")
                try:
                    author = User.objects.get(id=user_id, is_deleted=False)
                except Author.DoesNotExist:
                    raise PermissionDenied("Author does not exist.")

            elif user.is_authenticated and user.author:
                user_id = book_data.get('author')
                if user_id and user_id != user:
                    raise PermissionDenied(
                        "You can only create books for yourself.")
                author = user
            else:
                raise PermissionDenied(
                    "You do not have permission to create books.")
            book_data.pop('author', None)
            book = Book.objects.create(
                author=author,
                **book_data
            )
            book.save()
            return Response(
                {"message": "Book created successfully",
                 "data": Borr(book).data}, status=status.HTTP_201_CREATED
            )
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.error("Failed to create book: %s", str(e), exc_info=True)
            return Response({"error": "Failed to create book."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
