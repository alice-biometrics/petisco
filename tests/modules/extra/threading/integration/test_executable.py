from __future__ import annotations

from unittest.mock import Mock

import pytest

from petisco.extra.threading import Executable


def executable_func(value: str) -> str:
    return value


class ExecutableClass:
    def execute(self, value: str) -> str:
        return value


@pytest.mark.integration
class TestExecutable:
    def should_construct_with_function(self):
        executable = Executable(executable_func, ("executable 1",))
        assert executable.name == "executable_func"

    def should_construct_with_mock(self):
        mock = Mock(ExecutableClass)
        executable = Executable(mock, ("executable 1",))
        assert executable.name == "Mock:ExecutableClass"

    def should_construct_with_name(self):
        executable = Executable(executable_func, ("executable 1",), name="my_name")
        assert executable.name == "my_name"
