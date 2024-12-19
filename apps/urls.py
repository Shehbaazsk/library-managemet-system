from django.urls import include, path

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("books/", include("apps.books.urls")),
    path("borrow/", include("apps.borrow.urls"))
]
