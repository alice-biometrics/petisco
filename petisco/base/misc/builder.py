from typing import Any, NewType, cast

ClassType = NewType("ClassType", Any)


class Builder:
    def __init__(
        self, klass: ClassType, is_builder: bool = False, *args: Any, **kwargs: Any
    ) -> None:
        self.klass = klass
        self.args = args
        self.kwargs = kwargs
        self.is_builder = is_builder

    def build(self) -> ClassType:
        try:
            if self.is_builder:
                instance = self.klass.build(*self.args, **self.kwargs)
            else:
                instance = self.klass(*self.args, **self.kwargs)
        except Exception as exc:
            raise RuntimeError(
                f"Error instantiating {self.klass.__name__}\n{repr(exc)}"
            )

        return cast(ClassType, instance)
