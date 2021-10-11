import pytest


@pytest.fixture
def given_any_message():
    return "Hello world"


@pytest.fixture
def given_any_title():
    return "This is a title"


@pytest.fixture
def given_any_info_petisco():
    return {
        "app_name": "test",
        "app_version": "0.0.1",
        "petisco_version": "0.0.1",
        "environment": "Production",
    }


@pytest.fixture
def given_any_exception():
    return ValueError("Oops, something went wrong")


@pytest.fixture
def given_any_traceback():
    return """Traceback (most recent call last):
  File "e.py", line 7, in <module>
    raise TypeError("Again !?!")
TypeError: Again !?!
"""


@pytest.fixture
def given_long_traceback():
    return (
        """Traceback (most recent call last):
  File "e.py", line 7, in <module>
    raise TypeError("Again !?!")
TypeError: Again !?!
"""
        * 500
    )


@pytest.fixture
def given_any_input_parameters():
    return {"parameter_1": 1, "parameter_2": 2}
