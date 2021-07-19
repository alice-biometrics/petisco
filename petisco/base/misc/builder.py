from typing import Any


class Builder:
    def __init__(self, klass: Any, *args, **kwargs):
        self.klass = klass
        self.args = args
        self.kwargs = kwargs

    def build(self):
        return self.klass(*self.args, **self.kwargs)
