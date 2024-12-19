from django.db import models

from apps.utils.common_model import CommonModel


# Create your models here.
class BorrowRecord(CommonModel):

    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    # here we can also use relationship with user or author if needed instead of char field
    borrowed_by = models.CharField(max_length=255)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    # add more field

    def __str__(self):
        return self.book.title
