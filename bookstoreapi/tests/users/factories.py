import factory
from django.contrib.auth import get_user_model
from factory import Faker, post_generation


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: "person{0}@example.com".format(n))
    username = factory.Sequence(lambda n: "person_username{0}".format(n))
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("password")

    class Meta:
        model = get_user_model()
