from typing import Any, Optional

from pydantic import BaseModel

from bookstoreapi.apps.bookstores.models import Book
from bookstoreapi.apps.core.schema_fix import BookAPIModelSchema
from bookstoreapi.apps.users.schema import UserRetrieveSchema


class OKSchema(BaseModel):
    details: dict


class IdSchema(BaseModel):
    id: Any


class BookSchema(BookAPIModelSchema):
    created_by: Optional[UserRetrieveSchema]

    class Config:
        model = Book


class CreateBookSchema(BookAPIModelSchema):
    class Config:
        model = Book
        optional = ["created_by"]
