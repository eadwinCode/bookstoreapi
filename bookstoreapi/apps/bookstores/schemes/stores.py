from typing import Any, Optional

from django.db import transaction
from django.urls import reverse
from ninja_extra import service_resolver
from ninja_extra.controllers import RouteContext
from ninja_extra.exceptions import APIException
from ninja_schema import ModelSchema, Schema, model_validator
from pydantic.networks import AnyUrl
from typing_extensions import Annotated

from bookstoreapi.apps.bookstores.models import Store, StoreBook, StoreBookSubscription
from bookstoreapi.apps.bookstores.schemes.books import BookSchema
from bookstoreapi.apps.core.schema_fix import BookAPIModelSchema

# from bookstoreapi.apps.core.schema_fix import BookAPIModelSchema
from bookstoreapi.apps.users.schema import UserRetrieveSchema


class StoreCreateSchema(BookAPIModelSchema):
    class Config:
        model = Store
        include = [
            "name",
            "bio",
        ]

    @model_validator("name")
    def unique_name(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        if context.kwargs.get("store_id"):
            if not Store.objects.filter(
                name__contains=value_data, id=context.kwargs.get("store_id")
            ).exists():
                return value_data
        elif not Store.objects.filter(name__contains=value_data).exists():
            return value_data
        raise APIException("Store name exist")

    @transaction.atomic
    def create_store(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return Store.objects.create(**_data)


class StoreUpdateSchema(BookAPIModelSchema):
    class Config:
        model = Store
        include = [
            "name",
            "bio",
        ]
        optional = "__all__"

    @model_validator("name")
    def unique_name(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        if context.kwargs.get("store_id"):
            if not Store.objects.filter(
                name__contains=value_data, id=context.kwargs.get("store_id")
            ).exists():
                return value_data
        elif not Store.objects.filter(name__contains=value_data).exists():
            return value_data
        raise APIException("Store name exist")

    @transaction.atomic
    def create_store(self, **kwargs: Any):
        _data = self.dict(exclude_none=True)
        _data.update(kwargs)
        return Store.objects.create(**_data)


class StoreRetrieveSchema(ModelSchema):
    owner: UserRetrieveSchema

    class Config:
        model = Store
        include = ["name", "bio", "id"]


class StoreBookSchema(ModelSchema):
    borrowed_by: Optional[UserRetrieveSchema]
    store: Annotated[str, AnyUrl]
    book: BookSchema

    class Config:
        model = StoreBook

    @model_validator("store", mode="before")
    def store_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        value = reverse("store:detail", kwargs=dict(store_id=value_data.id))
        return context.request.build_absolute_uri(value)


class BorrowOrReturnStoreBookSchema(ModelSchema):
    borrowed_by: Optional[UserRetrieveSchema]
    store: Optional[Annotated[str, AnyUrl]]
    book: Optional[BookSchema]

    class Config:
        model = StoreBook
        include = ["borrowed_by", "store", "book"]

    @model_validator("store", mode="before")
    def store_validate(cls, value_data):
        context: RouteContext = service_resolver(RouteContext)
        value = reverse("store:detail", kwargs=dict(store_id=value_data.id))
        return context.request.build_absolute_uri(value)


class StoreBookSubscriptionSerializer(ModelSchema):
    store_book: StoreBookSchema
    subscriber: UserRetrieveSchema

    class Config:
        model = StoreBookSubscription
        include = ["store_book", "subscriber", "id"]


class StoreMessage(Schema):
    message: str
