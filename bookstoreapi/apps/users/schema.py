from datetime import datetime
from typing import List, Optional, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from ninja_extra import status
from ninja_extra.exceptions import APIException
from ninja_schema import ModelSchema, Schema, model_validator
from pydantic import validator

UserModel = get_user_model()


class GroupSchema(ModelSchema):
    class Config:
        model = Group
        include = ("name",)


class CreateUserSchema(ModelSchema):
    class Config:
        model = UserModel
        include = (
            "first_name",
            "last_name",
            "email",
            "username",
            "is_staff",
            "is_superuser",
            "password",
        )

    @model_validator("username")
    def unique_name(cls, value_data):
        if UserModel.objects.filter(username__icontains=value_data).exists():
            raise APIException(
                "Username already exist", status_code=status.HTTP_400_BAD_REQUEST
            )
        return value_data

    def create(self) -> Type[AbstractUser]:
        return UserModel.objects.create_user(**self.dict())


class CreateUserOutSchema(CreateUserSchema):
    token: str

    class Config:
        model = UserModel
        exclude = ("password",)


class UserRetrieveSchema(ModelSchema):
    groups: List[GroupSchema]

    class Config:
        model = UserModel
        include = ("email", "first_name", "last_name", "username", "id", "is_active")


class UserTokenOutSchema(Schema):
    token: str
    user: UserRetrieveSchema
    token_exp_date: Optional[datetime]


class EnableDisableUserSchema(Schema):
    user_id: str
    _user = None

    @validator(
        "user_id",
    )
    def validate_user_id(cls, value):
        user = UserModel.objects.filter(id=value).first()
        if user:
            cls._user = user
            return value
        raise ValueError("Invalid User Id")

    def update(self):
        self._user.is_active = not self._user.is_active
        self._user.save()
        return self._user

    def delete(self):
        _id = self._user.pk
        self._user.delete()
        return _id


class EnableDisableUserOutSchema(Schema):
    message: str
