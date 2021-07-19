from typing import Any


class Builder:
    def __init__(self, klass: Any, is_builder: bool = False, *args, **kwargs):
        self.klass = klass
        self.args = args
        self.kwargs = kwargs
        self.is_builder = is_builder

    def build(self):
        if self.is_builder:
            return self.klass.build(*self.args, **self.kwargs)
        return self.klass(*self.args, **self.kwargs)
