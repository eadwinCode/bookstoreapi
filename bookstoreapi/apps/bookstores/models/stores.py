import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
UserModel = get_user_model()


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    bio = models.TextField()
    owner = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_stores"
    )

    def __str__(self):
        return self.name


class StoreBook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="store_books"
    )
    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, related_name="store_books"
    )
    borrowed_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="books_borrowed",
        null=True,
        blank=True,
    )
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("store", "book")

    def __str__(self):
        return f"{self.store.name[:10]}-{self.book.name[:5]}"

    def save(self, *args, **kwargs):
        self.is_available = False if self.borrowed_by else True
        return super().save(*args, **kwargs)


class StoreBookSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store_book = models.ForeignKey(
        StoreBook, on_delete=models.CASCADE, related_name="subscribers"
    )
    subscriber = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="waiting_store_book"
    )

    class Meta:
        unique_together = ("store_book", "subscriber")

    def __str__(self):
        return f"{self.store_book.store.name[:10]}-{self.store_book.book.name[:5]}"
