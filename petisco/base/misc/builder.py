from typing import Any, Generic, Type, TypeVar, Union

T = TypeVar("T")


class Builder(Generic[T]):
    """
    Data structure that defines the creation of an instance from its arguments.
    """

    def __init__(
        self,
        klass: Type[T],
        name_constructor: Union[str, None] = None,
        is_builder: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.klass = klass
        self.args = args
        self.kwargs = kwargs
        self.name_constructor = name_constructor
        self.is_builder = is_builder

    def build(self) -> T:
        try:
            if self.name_constructor:
                constructor = getattr(self.klass, self.name_constructor)
                instance: T = constructor(*self.args, **self.kwargs)
            elif self.is_builder:
                instance: T = self.klass.build(*self.args, **self.kwargs)
            else:
                instance: T = self.klass(*self.args, **self.kwargs)
        except Exception as exc:
            raise RuntimeError(f"Error instantiating {self.klass.__name__}\n{repr(exc)}") from exc

        return instance
