from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.managers import UserManager
from apps.utils.common_model import CommonModel


class User(AbstractUser, CommonModel):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # add more field

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='author')
    bio = models.TextField(blank=True, null=True)

    # add more field

    def __str__(self):
        return self.user.email
