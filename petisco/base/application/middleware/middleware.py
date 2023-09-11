from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from loguru import logger
from meiga import AnyResult


class Middleware(ABC):
    """
    A base class to model your Middleware.
    A Middleware works before some operations (Controller and Subscriber) and also before returning the final result.
    """

    wrapped_class_name: Union[str, None] = None
    wrapped_class_input_arguments: Union[str, None] = None

    def set_data(
        self, wrapped_class_name: str, wrapped_class_input_arguments: Any
    ) -> None:
        self.wrapped_class_name = wrapped_class_name
        self.wrapped_class_input_arguments = wrapped_class_input_arguments

    @abstractmethod
    def before(self) -> None:
        pass

    @abstractmethod
    def after(self, result: AnyResult) -> None:
        pass

    def get_meta_from_input(self) -> Dict[str, Any]:
        # This method get info from legacy info_id model to keep compatibility
        meta = {}

        try:
            info_id = self.wrapped_class_input_arguments.get("info_id")
            if info_id and hasattr(info_id, "to_meta"):
                meta = info_id.to_meta().get("info_id", {})
        except Exception as exc:
            logger.error(
                f"Middleware error getting info_id on get_meta_from_input: {str(exc)}"
            )

        return meta
