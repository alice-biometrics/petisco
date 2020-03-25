import pytest
from flask import Response

from petisco.events.request_responded import RequestResponded


@pytest.fixture
def given_tuple_http_response():
    return {"message": "ok"}, 200


@pytest.fixture
def given_tuple_flask_http_response():
    return Response(), 200


@pytest.fixture
def given_tuple_flask_response():
    return Response()


@pytest.mark.unit
def test_should_construct_request_responded_from_a_tuple_http_response(
    given_tuple_http_response
):

    request_responded = RequestResponded(
        app_name="petisco",
        app_version="1.0.0",
        controller="my-controller",
        is_success=True,
        http_response=given_tuple_http_response,
        correlation_id="correlation-id",
        elapsed_time=1.0,
        additional_info=None,
    )

    assert request_responded.http_response["content"] == '{"message": "ok"}'
    assert request_responded.http_response["status_code"] == 200


@pytest.mark.unit
def test_should_construct_request_responded_from_a_tuple_flask_http_response(
    given_tuple_flask_http_response
):

    request_responded = RequestResponded(
        app_name="petisco",
        app_version="1.0.0",
        controller="my-controller",
        is_success=True,
        http_response=given_tuple_flask_http_response,
        correlation_id="correlation-id",
        elapsed_time=1.0,
        additional_info=None,
    )

    assert request_responded.http_response["content"] == "flask response"
    assert request_responded.http_response["status_code"] == 200


@pytest.mark.unit
def test_should_construct_request_responded_from_flask_http_response(
    given_tuple_flask_response
):

    request_responded = RequestResponded(
        app_name="petisco",
        app_version="1.0.0",
        controller="my-controller",
        is_success=True,
        http_response=given_tuple_flask_response,
        correlation_id="correlation-id",
        elapsed_time=1.0,
        additional_info=None,
    )

    assert request_responded.http_response["content"] == "flask response"
    assert request_responded.http_response["status_code"] == 200
