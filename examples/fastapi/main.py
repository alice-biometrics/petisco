from fastapi import FastAPI
from pydantic import BaseModel

from petisco import Uuid

app = FastAPI()


class User(BaseModel):
    id: Uuid


@app.post("/user")
def create_user(user: User) -> None:
    print(user.id)
    print(type(user.id))
    print(user.id.value)


@app.get("/user/{user_id}")
def retrieve_user(user_id: Uuid) -> None:
    print(type(user_id))
    return None
