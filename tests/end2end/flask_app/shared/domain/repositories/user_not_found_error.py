from meiga import Error


class UserNotFoundError(Error):
    def __init__(self, user_id):
        self.message = f"{self.__class__.__name__:s}: {user_id}"
