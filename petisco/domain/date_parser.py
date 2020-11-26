from datetime import datetime

from dateutil import parser


class DateParser:
    @staticmethod
    def datetime_from_str(value: str):
        if isinstance(value, str):
            value = parser.parse(value)
        return value

    @staticmethod
    def str_from_datetime(value: datetime):
        return str(value) if value is not None else None
