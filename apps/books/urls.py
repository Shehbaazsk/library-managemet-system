from django.urls import path

from apps.books.api.api_views import BookListCreateAPIView

urlpatterns = [
    path("", BookListCreateAPIView.as_view(), name="book-create-view"),
]
