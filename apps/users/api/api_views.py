
from rest_framework import filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.api.service import AuthorSerivce
from apps.users.models import Author
from apps.users.serializers import (
    AuthorRegisterSerializers,
    GetAuthorSerializer,
    ListAuthorSerializer,
)
from apps.utils.exceptions import CustomValidationError
from apps.utils.logger import get_logger
from apps.utils.permissions import IsOwnerOrAdmin

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
            return AuthorSerivce.register_author(data)

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


class AuthorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """API for retrieving a specific author by ID"""
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)
    serializer_class = GetAuthorSerializer
    lookup_field = 'id'
    queryset = Author.objects.all()

    def get_object(self):
        author = AuthorSerivce.get_author_by_user_id(self.kwargs['id'])
        if not (self.request.user.is_staff or author.user == self.request.user):
            raise PermissionDenied(
                "You do not have permission to access this author's data.")
        return author

    def put(self, request, *args, **kwargs):
        author = self.get_object()
        if not (self.request.user.is_staff or author.user == self.request.user):
            raise PermissionDenied(
                "You do not have permission to access this author's data.")
        return AuthorSerivce.update_author(author, request.data)

    def delete(self, request, *args, **kwargs):
        author = self.get_object()
        if not (self.request.user.is_staff or author.user == self.request.user):
            raise PermissionDenied(
                "You do not have permission to access this author's data.")
        return AuthorSerivce.delete_author(author)
