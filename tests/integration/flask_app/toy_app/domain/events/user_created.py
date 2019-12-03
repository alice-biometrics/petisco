from petisco import Event


class UserCreated(Event):
    user_id: str

    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__()
