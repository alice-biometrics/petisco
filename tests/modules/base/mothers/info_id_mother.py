from typing import Optional

import validators
from pydantic import validator

from petisco import InvalidUuid
from petisco.base.domain.ids.client_id import ClientId
from petisco.base.domain.ids.correlation_id import CorrelationId
from petisco.base.domain.ids.info_id import InfoId
from petisco.base.domain.ids.user_id import UserId


class InfoIdMother:
    @staticmethod
    def any():
        return InfoId(
            client_id=ClientId("ACME"),
            user_id=UserId.v4(),
            correlation_id=CorrelationId.v4(),
        )

    @staticmethod
    def with_redefined_user_id():
        class MyUserId(UserId):
            @validator("value")
            def validate_value(cls, value):
                if value is None or not validators.uuid(value):
                    if value is None or not len(value) != 16:
                        raise InvalidUuid(uuid_value=value)
                return value

        class MyInfoId(InfoId):
            user_id: Optional[MyUserId] = None

        return MyInfoId(
            client_id=ClientId("ACME"),
            user_id=MyUserId.v4(),
            correlation_id=CorrelationId.v4(),
        )
