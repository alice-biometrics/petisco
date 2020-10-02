from meiga import Error


class UserAlreadyExistError(Error):
    def __init__(self, user_id):
        self.message = f"{self.__class__.__name__:s}: [user_id: {user_id:s}]"
