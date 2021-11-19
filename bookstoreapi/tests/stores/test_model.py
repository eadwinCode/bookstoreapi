import pytest

from bookstoreapi.apps.bookstores.models import Store, StoreBook, StoreBookSubscription

py_test_mark = pytest.mark.django_db


@py_test_mark
class TestStoreModel:
    def test_create_model(self, user):
        store = Store.objects.create(name="New Store", owner=user)
        assert store.name == "New Store"
        assert store.owner == user


@py_test_mark
class TestStoreBookModel:
    def test_create_model(self, book, store):
        store = StoreBook.objects.create(store=store, book=book)
        assert store.is_available
        assert store.borrowed_by is None

    def test_store_book_not_available_on_borrowed(self, book, store, user):
        store = StoreBook.objects.create(store=store, book=book, borrowed_by=user)
        assert store.is_available is False
        assert store.borrowed_by == user

    def test_model_unique_constraint_works(self, book, store):
        StoreBook.objects.create(store=store, book=book)
        with pytest.raises(Exception) as ex:
            StoreBook.objects.create(store=store, book=book)
        assert "UNIQUE constraint failed" in str(ex)


@py_test_mark
class TestStoreBookSubscriptionModel:
    def test_create_model(self, store_book, user):
        store = StoreBookSubscription.objects.create(
            store_book=store_book, subscriber=user
        )
        assert store.store_book == store_book
        assert store.subscriber == user

    def test_model_unique_constraint_works(self, store_book, user):
        StoreBookSubscription.objects.create(store_book=store_book, subscriber=user)
        with pytest.raises(Exception) as ex:
            StoreBookSubscription.objects.create(store_book=store_book, subscriber=user)
        assert "UNIQUE constraint failed" in str(ex)
