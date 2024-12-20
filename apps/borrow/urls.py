from django.urls import path

from apps.borrow.api.api_views import BookBorrowCreateAPIView, BorrowBookReturnAPIView


urlpatterns = [
    path("", BookBorrowCreateAPIView.as_view(), name="book-create-view"),
    path("<int:borrow_record_id>/return/",
         BorrowBookReturnAPIView.as_view(), name="book-return-view")
]
