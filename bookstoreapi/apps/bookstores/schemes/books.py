from typing import Optional

from bookstoreapi.apps.bookstores.models import Book
from bookstoreapi.apps.core.schema_fix import BookAPIModelSchema
from bookstoreapi.apps.users.schema import UserRetrieveSchema


class BookSchema(BookAPIModelSchema):
    created_by: Optional[UserRetrieveSchema]

    class Config:
        model = Book


class CreateBookSchema(BookAPIModelSchema):
    class Config:
        model = Book
        optional = ["created_by"]
