from meiga import AnyResult

from petisco.base.application.middleware.middleware import Middleware


class PrintMiddleware(Middleware):
    def before(self) -> None:
        print(f"{self.wrapped_class_name} -> Start | Params {dict(self.wrapped_class_input_arguments)}")

    def after(self, result: AnyResult) -> None:
        print(f"{self.wrapped_class_name} -> End | {result}")
