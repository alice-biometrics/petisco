import copy

from petisco.base.misc.interface import Interface


class BasePattern(Interface):
    def with_info_id(self, info_id):
        base = copy.copy(self)
        base._set_info_id(info_id)
        return base

    def _set_info_id(self, info_id):
        if info_id is not None:
            self.info_id = info_id

    def get_info_id(self):
        if not hasattr(self, "info_id"):
            name = self.info().get("name")
            raise AttributeError(
                f"{name} needs info_id configuration. Please, use {name}.info_id() to get a valid object with info_id"
            )
        return self.info_id
