from django.urls import path

from apps.books.api.api_views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", BookListCreateAPIView.as_view(), name="book-create-view"),
    path("<int:id>/", BookRetrieveUpdateDestroyAPIView.as_view(),
         name="book-detail-view"),
]
