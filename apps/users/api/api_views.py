from django.db import transaction
from rest_framework import filters, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.models import Author, User
from apps.users.serializers import (
    AuthorRegisterSerializers,
    GetAuthorSerializer,
    ListAuthorSerializer,
)
from apps.utils.exceptions import CustomValidationError
from apps.utils.logger import get_logger

logger = get_logger(__name__)


class AuthorRegisterAPIView(GenericAPIView):
    """ Api for registering Author"""

    permission_classes = (AllowAny,)
    serializer_class = AuthorRegisterSerializers

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
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
                {"message": "User Created Successfully", }, status=status.HTTP_201_CREATED
            )
        except CustomValidationError as e:
            return Response({"error": e.detail}, status=e.status_code)
        except Exception as e:
            logger.error("Failed to create author: %s", str(e), exc_info=True)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuthorListAPIView(ListAPIView):
    """API for listing all authors"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ListAuthorSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__email', 'user__first_name']

    def get_queryset(self):

        return Author.objects.filter(
            user__is_delete=False,
            user__is_active=True
        ).select_related("user").only(
            "bio", "user__id", "user__email", "user__first_name", "user__last_name"
        ).order_by("-user__created_at")


class AuthorRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    """API for retrieving a specific author by ID"""
    permission_classes = (IsAuthenticated,)
    serializer_class = GetAuthorSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Author.objects.filter(
            user__id=self.kwargs['id'],
            user__is_delete=False,
            user__is_active=True
        ).select_related("user")

    def get_object(self):
        try:
            return self.get_queryset().get(user__id=self.kwargs['id'])
        except Author.DoesNotExist:
            raise NotFound(detail="Author not found", code=404)

    def perform_destroy(self, instance):
        instance.user.is_delete = True
        instance.user.save()
        instance.is_delete = True
        instance.save()
