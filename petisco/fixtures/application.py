from typing import Dict

import pytest


@pytest.fixture
def given_headers_provider():
    def _given_headers_provider(headers: Dict):
        return lambda: headers

    return _given_headers_provider
