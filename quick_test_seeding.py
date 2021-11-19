import os
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "bookstoreapi.settings.dev_sqlite"))
import django

django.setup()
logger = logging.getLogger(__name__)
from bookstoreapi.tests.users.factories import UserFactory, get_user_model
from bookstoreapi.tests.stores.factories import StoreFactory, StoreBookFactory, StoreBookSubscriptionFactory


def seed_data():
    # create 10 users for store owner
    logger.info("## Creating Store Owners...")
    store_owner = UserFactory.create_batch(10)
    logger.info("## Store Owners Created")
    store_books = []
    logger.info("## Creating Stores...")

    for idx, owner in enumerate(store_owner):
        store = StoreFactory(owner=owner)
        _store_books = StoreBookFactory.create_batch(50, store=store)
        store_books += _store_books
        logger.info(f"\t## Store: {idx + 1} created with {len(_store_books)} Books to it")

    logger.info("## All Stores Created")
    # create 20 users to subscribe to store books
    logger.info("## Running Store Subscription Started...")
    for idx, store_book in enumerate(store_books):
        logger.info(f"\t## Store Subscription: {idx + 1} created")
        subscriber = UserFactory()
        StoreBookSubscriptionFactory(subscriber=subscriber, store_book=store_book)


if __name__ == '__main__':
    logger.info('trying to populate database with dummy data')
    if get_user_model().objects.exists():
        logger.info('Database is already populated')
        exit()
    seed_data()
