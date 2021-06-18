from meiga import Result

from petisco.legacy import IAppService, AppService


class MyAppService(IAppService):
    def execute(self, *args, **kwargs) -> Result:
        pass


class AppServiceMother:
    @staticmethod
    def valid() -> AppService:
        return MyAppService()
