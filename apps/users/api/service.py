from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from apps.users.models import Author, User
from apps.utils.logger import get_logger

logger = get_logger(__name__)


def create_author(data):
    """
    Creates a User and associated Author.
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
        logger.error("Failed to create author: %s", str(e), exc_info=True)
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
