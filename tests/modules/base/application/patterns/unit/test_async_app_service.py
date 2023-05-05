from typing import Any, Dict

import pytest
from meiga import Result, isSuccess

from petisco import AsyncAppService


class MyAsyncAppService(AsyncAppService):
    async def execute(self, *args: Any, **kwargs: Any) -> Result:
        return isSuccess


@pytest.mark.unit
@pytest.mark.asyncio
class TestAsyncAppService:
    async def should_construct_and_execute(self):
        app_service = MyAsyncAppService()
        result = await app_service.execute()
        result.assert_success()
        assert app_service.info() == {"name": "MyAsyncAppService"}

    async def should_overwrite_info_method(self):
        class NoInfoAppService(MyAsyncAppService):
            def info(self) -> Dict[str, Any]:
                return {"message": "ok"}

        app_service = NoInfoAppService()

        assert app_service.info() == {"message": "ok"}
