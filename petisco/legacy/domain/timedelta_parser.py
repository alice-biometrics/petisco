from datetime import timedelta


class TimeDeltaParser:
    @staticmethod
    def ms_from_timedelta(value: timedelta):
        if isinstance(value, timedelta):
            value = value.microseconds / 1000
        return value
