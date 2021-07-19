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
def test_builder_success_with_both_args_and_kwargs():
    class MyClass:
        def __init__(self, arg1, arg2: str):
            self.arg1 = arg1
            self.arg2 = arg2

    builder = Builder(MyClass, "arg1", arg2="arg2")
    my_class = builder.build()

    assert isinstance(my_class, MyClass)
    assert my_class.arg1 == "arg1"
    assert my_class.arg2 == "arg2"


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
def test_builder_success_with_args():
    class MyClass:
        def __init__(self, arg1: str, arg2: str):
            self.arg1 = arg1
            self.arg2 = arg2

    builder = Builder(MyClass, "arg1", "arg2")
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

    with pytest.raises(TypeError):
        Builder(MyClass).build()
