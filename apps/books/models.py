from django.db import models

from apps.utils.common_model import CommonModel


# Create your models here.
class Book(CommonModel):

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        "users.user", on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField(default=0)

    # add more field

    def __str__(self):
        return self.title
