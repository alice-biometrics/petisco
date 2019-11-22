from petisco import Event


class UserCreated(Event):
    user_id: str
