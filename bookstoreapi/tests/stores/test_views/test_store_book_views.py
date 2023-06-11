import pytest
from django.core import mail
from django.urls import reverse
from ninja_extra import status, testing

from bookstoreapi.apps.bookstores.controllers import (
    StoreBookController,
    StoresController,
)
from bookstoreapi.apps.bookstores.models import Store, StoreBook
from bookstoreapi.tests.stores.factories import StoreBookFactory
from bookstoreapi.tests.test_utils import get_authentication_header
from bookstoreapi.tests.users.factories import UserFactory


@pytest.mark.django_db
class TestStoreView:
    def test_store_list_view_works(self, user, build_store_list):
        build_store_list(owner=user, batch_count=4)
        headers = get_authentication_header(user)
        client = testing.TestClient(StoresController)
        response = client.get('', headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("results")) == 4

    def test_users_can_create_store(self, user):
        headers = get_authentication_header(user)
        client = testing.TestClient(StoresController)
        payload = {
            "name": "New BookStore",
            "bio": "Some description",
        }
        response = client.post('', json=payload, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        assert Store.objects.filter(
            name="New BookStore"
        ).first(), "Store was not created"

    def test_store_owners_can_view_store_details(self, store):
        headers = get_authentication_header(store.owner)
        client = testing.TestClient(StoresController)

        response = client.get(f"/{store.id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert store.name in response.json()["name"]

    def test_store_owners_can_view_store_update_store_details(self, store):
        headers = get_authentication_header(store.owner)
        client = testing.TestClient(StoresController)

        payload = {
            "name": "New BookStore Updated",
            "bio": "Some description",
        }
        response = client.put(f"/{store.id}", json=payload, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert "New BookStore Updated" in response.json()["name"]

    def test_can_add_book_to_store(self, store):
        headers = get_authentication_header(store.owner)
        client = testing.TestClient(StoreBookController)
        payload = {
            "name": "BookStore Startup lol",
            "description": "Some description",
            "author": "Eadwin",
        }
        response = client.post(
            f"stores/{store.id}/book/create", json=payload, headers=headers
        )
        assert response.status_code == status.HTTP_201_CREATED

        response = client.post(
            f"stores/{store.id}/book/create", json=payload, headers=headers
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_store_owner_can_see_books_in_store(
        self, client, build_store_book_list, store
    ):
        build_store_book_list(store=store, batch_count=4)
        headers = get_authentication_header(
            store.owner, header_key="HTTP_AUTHORIZATION"
        )
        url = reverse("store:books", kwargs=dict(store_id=store.id))

        response = client.get(url, format="json", **headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 4

    def test_users_can_borrow_book_from_store_owner(self, client, store_book, user):
        headers = get_authentication_header(
            store_book.store.owner, header_key="HTTP_AUTHORIZATION"
        )

        url = reverse(
            "store:book-borrow",
            kwargs=dict(
                store_id=store_book.store.id,
                book_id=store_book.book.id,
                user_id=user.id,
            ),
        )

        response = client.post(url, {}, format="json", **headers)
        assert response.status_code == status.HTTP_200_OK
        assert StoreBook.objects.get(id=store_book.id).is_available is False

        response = client.post(url, {}, format="json", **headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_users_can_return_borrowed_book_from_store_owner(
        self, client, store, book, user
    ):
        headers = get_authentication_header(
            store.owner, header_key="HTTP_AUTHORIZATION"
        )
        store_book = StoreBookFactory(store=store, book=book, borrowed_by=user)

        url = reverse(
            "store:book-return", kwargs=dict(store_id=store.id, book_id=book.id)
        )

        response = client.post(url, {}, format="json", **headers)
        assert response.status_code == status.HTTP_200_OK
        assert StoreBook.objects.get(id=store_book.id).is_available
        response = client.post(url, {}, format="json", **headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_subscribed_users_on_a_book_store_gets_notified(
        self, client, store_book_subscription, user
    ):
        headers = get_authentication_header(
            store_book_subscription.store_book.store.owner,
            header_key="HTTP_AUTHORIZATION",
        )
        store_book_subscription.store_book.borrowed_by = UserFactory()
        store_book_subscription.store_book.save()

        url = reverse(
            "store:book-return",
            kwargs=dict(
                store_id=store_book_subscription.store_book.store.id,
                book_id=store_book_subscription.store_book.book.id,
            ),
        )

        response = client.post(url, {}, format="json", **headers)
        assert response.status_code == status.HTTP_200_OK
        assert len(mail.outbox) > 0
