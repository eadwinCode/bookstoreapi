import traceback
from typing import Any, Optional

from ninja_schema import ModelSchema


class BookAPIModelSchema(ModelSchema):
    # _output_schema = None

    def create(self, **kwargs: Any) -> Any:
        """Override this function if you have a way of creating an object."""
        model_class = self.Config.model  # type: ignore
        data = self.dict()
        data.update(kwargs)

        try:
            instance = model_class._default_manager.create(**data)
            return instance
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                "Got a `TypeError` when calling `%s.%s.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.%s.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception was:\n %s"
                % (
                    model_class.__name__,
                    model_class._default_manager.name,
                    model_class.__name__,
                    model_class._default_manager.name,
                    self.__class__.__name__,
                    tb,
                )
            )
            raise TypeError(msg)

    def update(self, instance: Any, **kwargs: Any) -> Any:
        """Override this function if you have a way of creating an object."""
        if not instance:
            raise Exception("Instance is required")
        data = self.dict(exclude_none=True)
        data.update(kwargs)
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def save(self, instance: Optional[Any] = None, **kwargs: Any) -> Any:
        if instance:
            result = self.update(instance, **kwargs)
            assert result is not None, "`update()` did not return an object instance."
        else:
            result = self.create(**kwargs)
            assert result is not None, "`create()` did not return an object instance."

        return result
