from django.contrib.auth import get_user_model
from ninja_jwt.tokens import SlidingToken

User = get_user_model()


def get_authentication_header(user, admin_user=False, header_key="Authorization"):
    if admin_user:
        user.is_superuser = True
        user.save()

    token = SlidingToken.for_user(user)
    user_credential = {header_key: "Bearer " + str(token)}
    return user_credential
