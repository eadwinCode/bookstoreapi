import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
UserModel = get_user_model()


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_books"
    )

    class Meta:
        unique_together = ("name", "author")

    def __str__(self):
        return self.name
