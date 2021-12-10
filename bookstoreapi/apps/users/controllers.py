from datetime import datetime

from django.contrib.auth import get_user_model
from ninja_extra import api_controller, route, status
from ninja_extra.permissions import IsAdminUser, IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import TokenObtainSlidingController, schema
from ninja_jwt.tokens import SlidingToken

from bookstoreapi.apps.users.schema import (
    CreateUserSchema,
    EnableDisableUserOutSchema,
    EnableDisableUserSchema,
    UserTokenOutSchema,
)

User = get_user_model()


@api_controller("/api/auth", tags=["users"], auth=JWTAuth())
class UserController:
    @route.post(
        "/create", response={201: UserTokenOutSchema}, url_name="user-create", auth=None
    )
    def create_user(self, user_schema: CreateUserSchema):
        user = user_schema.create()
        token = SlidingToken.for_user(user)
        return UserTokenOutSchema(
            user=user,
            token=str(token),
            token_exp_date=datetime.utcfromtimestamp(token["exp"]),
        )

    @route.put(
        "/{int:pk}/enable-disable",
        permissions=[IsAuthenticated, IsAdminUser],
        response=EnableDisableUserOutSchema,
        url_name="user-enable-disable",
    )
    def enable_disable_user(self, pk: int):
        user_schema = EnableDisableUserSchema(user_id=str(pk))
        user_schema.update()
        return EnableDisableUserOutSchema(message="Action Successful")

    @route.delete(
        "/{int:pk}/delete",
        permissions=[IsAuthenticated, IsAdminUser],
        response=EnableDisableUserOutSchema,
        url_name="user-delete",
    )
    def delete_user(self, pk: int):
        user_schema = EnableDisableUserSchema(user_id=str(pk))
        user_schema.delete()
        return self.create_response("", status_code=status.HTTP_204_NO_CONTENT)


@api_controller("/api/auth", tags=["auth"])
class UserTokenController(TokenObtainSlidingController):
    auto_import = True

    @route.post("/login", response=UserTokenOutSchema, url_name="login")
    def obtain_token(self, user_token: schema.TokenObtainSlidingSerializer):
        user = user_token._user
        token = SlidingToken.for_user(user)
        return UserTokenOutSchema(
            user=user,
            token=str(token),
            token_exp_date=datetime.utcfromtimestamp(token["exp"]),
        )

    @route.post(
        "/api-token-refresh",
        response=schema.TokenRefreshSlidingSerializer,
        url_name="refresh",
    )
    def refresh_token(self, refresh_token: schema.TokenRefreshSlidingSchema):
        refresh = schema.TokenRefreshSlidingSerializer(**refresh_token.dict())
        return refresh
