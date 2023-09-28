from fastapi import FastAPI
from pydantic import BaseModel

from petisco import Uuid

app = FastAPI()


class User(BaseModel):
    id: Uuid


@app.post("/user")
def create_user(user: User) -> None:
    print(f"{user.id=}")
    print(f"type {type(user.id)}")
    print(f"value {user.id.value}")
    print(f"uuid {user.id}")

    print(f"{Uuid.v4()}")


@app.get("/user/{user_id}")
def retrieve_user(user_id: Uuid) -> None:
    print(type(user_id))

    # converted = Uuid(user_id)
    # print(type(converted))

    return None
