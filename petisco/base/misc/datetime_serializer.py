from datetime import datetime

from pydantic import PlainSerializer

from petisco.base.domain.message.message import TIME_FORMAT


def serialize_datetime(value: datetime) -> str:
    return value.strftime(TIME_FORMAT)


DatetimeSerializer = PlainSerializer(serialize_datetime)
