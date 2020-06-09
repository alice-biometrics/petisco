#!/usr/bin/env python
from petisco import StringValueObject
from meiga import Error


class UsernameIsNotLowerError(Error):
    pass


class Username(StringValueObject):
    def guard(self):
        self._ensure_is_lowercase()

    def _ensure_is_lowercase(self):
        if not self.value.islower():
            raise UsernameIsNotLowerError()
