from typing import Any, Dict

import pytest
from meiga import Result, isSuccess

from petisco import AppService


class MyAppService(AppService):
    def execute(self, *args: Any, **kwargs: Any) -> Result:
        return isSuccess


@pytest.mark.unit
class TestAppService:
    def should_construct_and_execute(self):
        app_service = MyAppService()
        result = app_service.execute()
        result.assert_success()
        assert app_service.info() == {"name": "MyAppService"}

    def should_overwrite_info_method(self):
        class NoInfoAppService(MyAppService):
            def info(self) -> Dict[str, Any]:
                return {"message": "ok"}

        app_service = NoInfoAppService()

        assert app_service.info() == {"message": "ok"}
