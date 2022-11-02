from typing import Any

import pytest

from petisco import Builder


@pytest.mark.unit
def test_builder_success_without_args_and_kwargs():
    class MyClass:
        pass

    builder = Builder(MyClass)

    assert isinstance(builder.build(), MyClass)


@pytest.mark.unit
def test_builder_success_with_args_and_kwargs_default():
    class MyClass:
        def __init__(self, arg1: str = "default", arg2: str = "default"):
            self.arg1 = arg1
            self.arg2 = arg2

    builder = Builder(MyClass)
    my_class = builder.build()

    assert isinstance(my_class, MyClass)
    assert my_class.arg1 == "default"
    assert my_class.arg2 == "default"


@pytest.mark.unit
def test_builder_success_with_kwargs():
    class MyClass:
        def __init__(self, arg1: str, arg2: str):
            self.arg1 = arg1
            self.arg2 = arg2

    builder = Builder(MyClass, arg1="arg1", arg2="arg2")
    my_class = builder.build()

    assert isinstance(my_class, MyClass)
    assert my_class.arg1 == "arg1"
    assert my_class.arg2 == "arg2"


@pytest.mark.unit
def test_builder_fail_and_raise_an_error_when_rquired_positional_argument_is_not_given():
    class MyClass:
        def __init__(self, arg1, arg2: str = "default"):
            self.arg1 = arg1
            self.arg2 = arg2

    with pytest.raises(RuntimeError):
        Builder(MyClass).build()


@pytest.mark.unit
def test_builder_success_with_builder_class():
    class MyClass:
        @staticmethod
        def build():
            return MyClass()

    builder = Builder(MyClass, is_builder=True)
    my_class = builder.build()

    assert isinstance(my_class, MyClass)


@pytest.mark.unit
def test_builder_success_with_builder_class_with_arguments():
    class MyClass:
        def __init__(self, arg1: str, arg2: str):
            self.arg1 = arg1
            self.arg2 = arg2

        @staticmethod
        def build(*args: Any, **kwargs: Any):
            return MyClass(*args, **kwargs)

    builder = Builder(MyClass, is_builder=True, arg1="arg1", arg2="arg2")
    my_class = builder.build()

    assert isinstance(my_class, MyClass)
    assert my_class.arg1 == "arg1"
    assert my_class.arg2 == "arg2"


@pytest.mark.unit
def test_builder_raise_an_exception_with_error_in_constructor():
    class MyClass:
        def __init__(self):
            raise TypeError("My Exception")

    with pytest.raises(RuntimeError) as excinfo:
        builder = Builder(MyClass)
        builder.build()
    assert "Error instantiating MyClass" in str(excinfo.value)


@pytest.mark.unit
def test_builder_raise_an_exception_with_error_in_builder_class():
    class MyClass:
        @staticmethod
        def build():
            raise TypeError("My Exception")

    with pytest.raises(RuntimeError) as excinfo:
        builder = Builder(MyClass, is_builder=True)
        builder.build()
    assert "Error instantiating MyClass" in str(excinfo.value)


@pytest.mark.unit
def test_builder_success_with_name_constructor_class():
    class MyClass:
        @staticmethod
        def build():
            return MyClass()

    builder = Builder(MyClass, name_constructor="build")
    my_class = builder.build()

    assert isinstance(my_class, MyClass)


@pytest.mark.unit
def test_builder_success_with_name_constructor_class_with_my_name_constructor_name_staticmethod():
    class MyClass:
        @staticmethod
        def my_name_constructor_name():
            return MyClass()

    builder = Builder(MyClass, name_constructor="my_name_constructor_name")
    my_class = builder.build()

    assert isinstance(my_class, MyClass)


@pytest.mark.unit
def test_builder_success_with_name_constructor_class_with_arguments():
    class MyClass:
        def __init__(self, arg1: str, arg2: str):
            self.arg1 = arg1
            self.arg2 = arg2

        @staticmethod
        def build(*args: Any, **kwargs: Any):
            return MyClass(*args, **kwargs)

    builder = Builder(MyClass, name_constructor="build", arg1="arg1", arg2="arg2")
    my_class = builder.build()

    assert isinstance(my_class, MyClass)
    assert my_class.arg1 == "arg1"
    assert my_class.arg2 == "arg2"


@pytest.mark.unit
def test_builder_raise_an_exception_with_error_in_name_constructor_class():
    class MyClass:
        @staticmethod
        def build():
            raise TypeError("My Exception")

    with pytest.raises(RuntimeError) as excinfo:
        builder = Builder(MyClass, name_constructor="build")
        builder.build()
    assert "Error instantiating MyClass" in str(excinfo.value)
