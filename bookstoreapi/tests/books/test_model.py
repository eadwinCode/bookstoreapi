import pytest

from bookstoreapi.apps.bookstores.models import Book

py_test_mark = pytest.mark.django_db


@py_test_mark
class TestBookModel:
    def test_create_model(self, user):
        book = Book.objects.create(
            name="New Book", author="New Author", created_by=user
        )
        assert book.name == "New Book"
        assert book.author == "New Author"

    def test_model_unique_constraint_works(self, user):
        Book.objects.create(name="New Book", author="New Author", created_by=user)
        with pytest.raises(Exception) as ex:
            Book.objects.create(name="New Book", author="New Author", created_by=user)
        assert "UNIQUE constraint failed" in str(ex)
