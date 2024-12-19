from uuid import uuid4

from django.db import models
from rest_framework import serializers


class CommonModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False,)
    # INSTEAD OF EXPOSING PK WE CAN USE UUID
    # uuid = models.UUIDField(default=uuid4, unique=True)

    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommonModelSerializer(serializers.ModelSerializer):
    """Serializer for the CommonModel fields"""

    class Meta:
        # fields = ["uuid", "is_active", "is_delete", "created_at", "updated_at"]
        fields = ["id", "is_active", "is_delete", "created_at", "updated_at"]
