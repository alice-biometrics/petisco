import inspect
from typing import Dict, TypeVar, Callable

from deprecation import deprecated

from petisco.application.interface_app_service import IAppService
from petisco.application.singleton import Singleton

AppService = TypeVar("AppService", bound=IAppService)


class AppServices(metaclass=Singleton):
    def __init__(self, app_services: Dict[str, AppService] = None):
        self._app_services = app_services if app_services else {}

    def get_info(self):
        return {
            name: app_service.info() for name, app_service in self._app_services.items()
        }

    @staticmethod
    def info():
        return AppServices.get_instance().get_info()

    @staticmethod
    def load(provider: Callable):
        repositories = provider()
        return AppServices(repositories)

    @staticmethod
    def get_instance():
        try:
            return AppServices()
        except Exception as e:  # noqa E722
            frame_info = inspect.stack()[1]
            raise ImportError(
                f"AppServices must be configured. If not, you cannot obtain app serives\n"
                f"Following code must be executed after AppServices initialization:\n"
                f"\tfilename: {frame_info.filename}\n"
                f"\tlineno: {frame_info.lineno}\n"
                f"\tfunction: {frame_info.function}\n"
                f"\tcode_context: {frame_info.code_context}\n\n"
            )

    def add(self, name: str, app_service: AppService):
        if name in self._app_services:
            raise NameError(f"AppService {name} is already added to AppServices")
        self._app_services[name] = app_service

    def remove(self, name: str):
        if name in self._app_services:
            del self._app_services[name]
        else:
            raise IndexError(f"AppService cannot be removed. {name} not exists")

    @staticmethod
    def get(name: str) -> AppService:
        app_services = AppServices.get_instance()._app_services
        if app_services is None:
            raise ValueError(
                "AppServices: no app service has been declared. Please, initialize it (i.e AppServices.from_provider(provider_func))"
            )
        app_service = app_services.get(name)
        if not app_service:
            raise ValueError(
                f"AppServices: {name} app service is not defined.  Please, add it (i.e AppServices.from_provider(provider_func))"
            )
        return app_service

    @staticmethod
    @deprecated("This method is deprecated. Please, use AppServices.load")
    def from_provider(provider: Callable):
        return AppServices.load(provider)
