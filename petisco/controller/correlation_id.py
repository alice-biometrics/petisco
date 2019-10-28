import hashlib
import random
import string
from datetime import datetime


class CorrelationId(str):
    def __init__(self, value):
        super(CorrelationId, self).__init__()
        self.value = value

    @staticmethod
    def generate(func_name: str = ""):
        datetime_string = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
        data_to_hash = (
            func_name + CorrelationId.random_string(10) + " " + datetime_string
        )
        return CorrelationId(CorrelationId.hash_string(data_to_hash))

    @staticmethod
    def hash_string(string: str):
        """
        Return a SHA-256 hash of the given string
        """
        return hashlib.sha256(string.encode("utf-8")).hexdigest()[:5]

    @staticmethod
    def random_string(string_length: int):
        letters = string.ascii_letters
        return "".join(random.choice(letters) for i in range(string_length))
