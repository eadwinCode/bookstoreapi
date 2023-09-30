from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import transaction
from ninja_extra import api_controller, route, status
from ninja_extra.pagination import (
    PageNumberPaginationExtra,
    PaginatedResponseSchema,
    paginate,
)
from ninja_extra.permissions import IsAuthenticated
from ninja_extra.shortcuts import get_object_or_exception
from ninja_jwt.authentication import JWTAuth

from bookstoreapi.apps.bookstores.mixins import StoryBookQuerySetMixin
from bookstoreapi.apps.bookstores.models import StoreBook, StoreBookSubscription
from bookstoreapi.apps.bookstores.schemes.stores import StoreBookSubscriptionSerializer
from bookstoreapi.apps.bookstores.schemes.books import IdSchema, OKSchema

User = get_user_model()


@api_controller("/books", auth=JWTAuth(), permissions=[IsAuthenticated])
class StoryBookSubscribeController(StoryBookQuerySetMixin):
    @route.post(
        "/{uuid:store_book_id}/{int:user_id}/subscriber",
        url_name="subscribe",
        response=IdSchema,
    )
    @transaction.atomic
    def subscribe(self, store_book_id: UUID, user_id: int):
        user = get_object_or_exception(
            User,
            id=user_id,
            error_message="User with id {} does not exist".format(user_id),
        )
        store_book = get_object_or_exception(
            StoreBook,
            id=store_book_id,
            store__owner=self.context.request.user,
            error_message="StoreBook with id {} does not exist".format(user_id),
        )
        subscription = StoreBookSubscription.objects.create(
            store_book=store_book, subscriber=user
        )
        return dict(id=subscription.pk)

    @route.post(
        "/{uuid:store_book_subscription_id}/unsubscribe",
        url_name="unsubscribe",
        response={status.HTTP_204_NO_CONTENT: OKSchema},
    )
    @transaction.atomic
    def unsubscribe(self, store_book_subscription_id: UUID):
        instance = get_object_or_exception(
            StoreBookSubscription,
            id=store_book_subscription_id,
            error_message="StoreBookSubscription with id {} does not exist".format(
                store_book_subscription_id
            ),
        )
        instance.delete()
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)

    @route.get(
        "/{uuid:store_id}/subscribers",
        response=PaginatedResponseSchema[StoreBookSubscriptionSerializer],
        url_name="subscribers",
    )
    @paginate(PageNumberPaginationExtra)
    def list(self, store_id: UUID):
        return self.get_queryset().filter(store_book__store_id=store_id)
