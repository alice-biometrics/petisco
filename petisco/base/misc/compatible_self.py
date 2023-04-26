import sys


def compatible_self(expected_type: str):
    if sys.version_info >= (3, 10):
        from typing import Self

        return Self
    else:
        return expected_type
