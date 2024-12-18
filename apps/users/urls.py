from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api.api_views import (
    AuthorListAPIView,
    AuthorRegisterAPIView,
    AuthorRetrieveDestroyAPIView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", AuthorRegisterAPIView.as_view(), name="register"),
    path('authors/', AuthorListAPIView.as_view(), name='author-list'),
    path('authors/<int:id>/', AuthorRetrieveDestroyAPIView.as_view(),
         name='author-retrieve-delete'),
]
