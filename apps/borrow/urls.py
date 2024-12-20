from django.urls import path

from apps.borrow.api.api_views import BookBorrowCreateAPIView


urlpatterns = [
    path("", BookBorrowCreateAPIView.as_view(), name="book-create-view"),
]
