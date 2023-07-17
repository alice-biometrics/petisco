import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from petisco import DomainEvent

app = FastAPI(title="test-app")


class UserCreated(DomainEvent):
    name: str
    age: int


@app.webhooks.post("/new-user")
def on_user_created(body: UserCreated):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.
    """


@pytest.mark.unit
def test_fastapi_app_is_well_instantiated_with_webhooks():
    with TestClient(app):
        pass
