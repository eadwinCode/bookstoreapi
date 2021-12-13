from django.contrib.auth import get_user_model
from ninja_extra import api_controller, route, status
from ninja_extra.controllers import Detail, Id
from ninja_extra.pagination import (
    PageNumberPaginationExtra,
    PaginatedResponseSchema,
    paginate,
)
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from pydantic.types import UUID4

from bookstoreapi.apps.bookstores.mixins import StoreViewMixin
from bookstoreapi.apps.bookstores.models import Store, StoreBook
from bookstoreapi.apps.bookstores.schemes.books import BookSchema, CreateBookSchema
from bookstoreapi.apps.bookstores.schemes.stores import (
    BorrowOrReturnStoreBookSchema,
    StoreBookSchema,
    StoreCreateSchema,
    StoreMessage,
    StoreRetrieveSchema,
    StoreUpdateSchema,
)
from bookstoreapi.apps.bookstores.tasks import process_subscription_notification
from bookstoreapi.apps.core.logger import logger


@api_controller("/stores", permissions=[IsAuthenticated], auth=JWTAuth())
class StoresController(StoreViewMixin):
    @route.post("", response=[Id, Detail(status_code=400)], url_name="create")
    def create_store(self, store: StoreCreateSchema):
        try:
            store = store.create_store(owner=self.context.request.user)
            return self.Id(store.pk)
        except Exception as ex:
            logger.error(f"failed to create store: {ex}")
            return Detail(str(ex), status_code=400)

    @route.get(
        "",
        response=PageNumberPaginationExtra.get_response_schema(StoreRetrieveSchema),
        url_name="list",
    )
    @paginate(PageNumberPaginationExtra)
    def list_stores(self):
        return self.get_queryset()

    @route.get("/{uuid:store_id}", response=StoreRetrieveSchema, url_name="detail")
    def retrieve_store(self, store_id: str):
        store = self.get_object_or_exception(
            self.get_queryset(),
            id=store_id,
            error_message="Store with id {} does not exist".format(store_id),
        )
        return store

    @route.generic(
        "/{uuid:store_id}",
        methods=["PUT"],
        response=StoreRetrieveSchema,
        url_name="update",
    )
    def update_store(self, store_id: str, store_schema: StoreUpdateSchema):
        store = self.get_object_or_exception(self.get_queryset(), id__exact=store_id)
        store_schema.update(store)
        return store

    @route.delete(
        "/{uuid:store_id}", url_name="destroy", response=Detail(status_code=204)
    )
    def delete_store(self, store_id: str):
        store = self.get_object_or_exception(
            self.get_queryset(),
            id=store_id,
            error_message="Store with id {} does not exist".format(store_id),
        )
        store.delete()
        return self.create_response(
            "Item Deleted", status_code=status.HTTP_204_NO_CONTENT
        )


@api_controller(
    "/stores/{uuid:store_id}", permissions=[IsAuthenticated], auth=JWTAuth()
)
class StoreBookController(StoreViewMixin):
    User = get_user_model()
    base_url = ""

    @route.get(
        "/books",
        response=PaginatedResponseSchema[StoreBookSchema],
        url_name="books",
    )
    @paginate(PageNumberPaginationExtra)
    def list_store_books(self, store_id: UUID4):
        stores = StoreBook.objects.filter(
            store_id=store_id, store__owner_id=self.context.request.user
        )
        return stores

    @route.post(
        "/book/create",
        response=[(201, BookSchema), Detail(status_code=400)],
        url_name="book-create",
    )
    def add_store_book(self, store_id: UUID4, book: CreateBookSchema):
        try:
            store = self.get_object_or_exception(
                Store,
                id=store_id,
                error_message="Store with id {} does not exist".format(store_id),
            )
            book = book.save(created_by=self.context.request.user)
            StoreBook.objects.create(book=book, store=store)
            return 201, book
        except Exception as ex:
            return self.create_response(
                str(ex), status_code=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self, store_id: UUID4, book_id: UUID4):
        store_book = self.get_object_or_none(
            StoreBook.objects.select_related("store", "book"),
            store__id=store_id,
            book__id=book_id,
            store__owner_id=self.context.request.user,
        )
        return store_book

    @route.post(
        "/book/{uuid:book_id}/borrow/{int:user_id}/",
        response={200: BorrowOrReturnStoreBookSchema, 400: dict},
        url_name="book-borrow",
    )
    def borrow_store_books(self, store_id: UUID4, book_id: UUID4, user_id: int):
        store_book = self.get_object(store_id, book_id)

        user = self.get_object_or_exception(
            self.User,
            id=user_id,
            error_message="User with id {} does not exist".format(user_id),
        )
        if store_book.borrowed_by:
            return self.create_response(
                message="Borrowed book can not be reassigned. It must be returned",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        store_book.borrowed_by = user
        store_book.save()
        return store_book

    @route.post(
        "/book/{uuid:book_id}/return",
        response={200: StoreMessage, 400: StoreMessage},
        url_name="book-return",
    )
    def return_store_books(self, store_id: UUID4, book_id: UUID4):
        store_book = self.get_object(store_id, book_id)
        if store_book.borrowed_by:
            store_book.borrowed_by = None
            store_book.save()
            process_subscription_notification(store_book_id=store_book.id)
            return status.HTTP_200_OK, StoreMessage(message="It is already returned")
        return status.HTTP_400_BAD_REQUEST, StoreMessage(
            message="It is already returned"
        )
