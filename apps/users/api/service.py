
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.users.models import Author, User
from apps.users.serializers import GetAuthorSerializer
from apps.utils.exceptions import CustomValidationError
from apps.utils.logger import get_logger

logger = get_logger(__name__)


class AuthorSerivce:
    """
    Service class for Author operations
    """

    @staticmethod
    def register_author(data):
        """
        Register a new Author with user and author model.
        """
        try:
            user_data = {
                "email": data["email"],
                "password": data["password"],
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
            }
            author_data = {
                "bio": data.get("bio"),
            }
            with transaction.atomic():
                user = User.objects.create_user(**user_data)
                author = Author.objects.create(user=user, **author_data)
            return Response(
                {"message": "User Created Successfully"}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error("Failed to register author: %s",
                         str(e), exc_info=True)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def get_author_by_user_id(user_id):
        """
        Retrieve the Author by user ID.
        """
        try:
            return Author.objects.select_related("user").get(
                user__id=user_id,
                user__is_delete=False,
                user__is_active=True
            )
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found", code=404)

    @staticmethod
    def update_user(user_instance, validated_data):
        """
        Update user data
        """

        for field, value in validated_data.items():
            if hasattr(user_instance, field) and getattr(user_instance, field) != value:
                setattr(user_instance, field, value)

        user_instance.save()

    @staticmethod
    def update_author(author_instance, validated_data):
        """
        Update author data
        """
        user_data = validated_data.pop('user', {})

        if user_data:
            if user_data.get('email'):
                if User.objects.filter(email=user_data.get('email'), is_delete=False).exclude(id=author_instance.user_id).exists():
                    raise CustomValidationError(
                        "A user with this email already exists."
                    )
            AuthorSerivce.update_user(author_instance.user, user_data)

        for field, value in validated_data.items():
            if hasattr(author_instance, field) and getattr(author_instance, field) != value:
                setattr(author_instance, field, value)

        author_instance.save()

        return Response(
            {"message": "Author updated successfully",
             "data": GetAuthorSerializer(author_instance).data}, status=status.HTTP_202_ACCEPTED
        )

    @staticmethod
    def delete_author(author):
        """
        Delete an author
        """
        try:
            author.user.is_delete = True
            author.user.save()
            return Response(
                {"message": "Author deleted successfully"}, status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.error("Failed to delete author: %s", str(e), exc_info=True)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
