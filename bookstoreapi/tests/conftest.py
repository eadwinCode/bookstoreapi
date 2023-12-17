from random import randint, random

import pytest
from django.test import Client

from bookstoreapi.tests.books.factories import BookFactory
from bookstoreapi.tests.stores.factories import (
    StoreBookFactory,
    StoreBookSubscriptionFactory,
    StoreFactory,
)
from bookstoreapi.tests.users.factories import UserFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def app_admin():
    user = UserFactory(
        is_superuser=True, is_staff=True, username="admin", email="admin@dmin.com"
    )
    return user


@pytest.fixture
def random_email():
    return "email{}@email.com".format(random())


@pytest.fixture
def random_username():
    return "username{}".format(random())


@pytest.fixture
def random_id(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def store():
    return StoreFactory()


@pytest.fixture
def store_book():
    return StoreBookFactory()


@pytest.fixture
def store_book_subscription():
    return StoreBookSubscriptionFactory()


@pytest.fixture
def book():
    return BookFactory()


@pytest.fixture
def build_store_book_list():
    def _wrap(owner=None, store=None, batch_count=5):
        store_books = []
        user = store.owner if store else owner or UserFactory()
        store = store or StoreFactory(owner=user)
        books = BookFactory.create_batch(batch_count, created_by=user)
        for book in books:
            store_books.append(StoreBookFactory(book=book, store=store))
        return store_books

    return _wrap


@pytest.fixture
def build_store_book_subscription_list():
    def _wrap(owner=None, batch_count=5):
        store_books, store_book_subscriptions = [], []
        user = owner or UserFactory()
        store = StoreFactory(owner=user)
        books = BookFactory.create_batch(batch_count, created_by=user)
        users = UserFactory.create_batch(batch_count)

        for book in books:
            store_books.append(StoreBookFactory(book=book, store=store))

        for store_book, user in zip(store_books, users):
            store_book_subscriptions.append(
                StoreBookSubscriptionFactory(store_book=store_book, subscriber=user)
            )
        return store_book_subscriptions, store_books, books

    return _wrap


@pytest.fixture
def build_store_list():
    def _wrap(owner=None, batch_count=5):
        user = owner or UserFactory()
        stores = StoreFactory.create_batch(batch_count, owner=user)
        return stores

    return _wrap
