import sys
from datetime import datetime

import pytest
from pydantic import BaseModel, Field

from petisco import DatetimeSerializer


@pytest.mark.unit
class TestDatetimeSerializer:
    @pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires Python 3.9 or higher")
    def should_serialize_datetime(self) -> None:  # noqa
        from typing import Annotated  # noqa (available in Python 3.9)

        class MyModel(BaseModel):
            created_at: Annotated[datetime, DatetimeSerializer] = Field(default_factory=datetime.utcnow)

        model = MyModel()

        assert isinstance(model.model_dump()["created_at"], str)
