from datetime import datetime
from typing import Annotated

import pytest
from pydantic import BaseModel, Field

from petisco import DatetimeSerializer


@pytest.mark.unit
class TestDatetimeSerializer:
    def should_serialize_datetime(self) -> None:  # noqa
        class MyModel(BaseModel):
            created_at: Annotated[datetime, DatetimeSerializer] = Field(
                default_factory=datetime.utcnow
            )

        model = MyModel()

        assert isinstance(model.model_dump()["created_at"], str)
