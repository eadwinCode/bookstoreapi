from typing import Any

from django.db.models import QuerySet

from bookstoreapi.apps.bookstores.models import Store, StoreBookSubscription


class StoreViewMixin:
    request: Any

    def get_queryset(self) -> QuerySet[Store]:
        return Store.objects.filter(owner_id=self.context.request.user)


class StoryBookQuerySetMixin:
    request: Any

    def get_queryset(self):
        return StoreBookSubscription.objects.select_related(
            "store_book", "subscriber"
        ).filter(store_book__store__owner=self.context.request.user)
