import hashlib

from meiga import Error

from petisco.domain.value_objects.value_object import ValueObject


class SignatureAlgorithmIsNotAvailableError(Error):
    def __init__(self, message):
        self.message = message


class SignatureAlgorithm(ValueObject):
    @staticmethod
    def sha256():
        return SignatureAlgorithm("sha256")

    @staticmethod
    def sha512():
        return SignatureAlgorithm("sha512")

    def __init__(self, value: str):
        self.value = value
        self.available_hash_algoritmhs = {
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512,
        }
        super(SignatureAlgorithm, self).__init__()

    def guard(self):
        if self.value not in self.available_hash_algoritmhs.keys():
            raise SignatureAlgorithmIsNotAvailableError(self.value)

    def get_algorithm(self):
        return self.available_hash_algoritmhs.get(self.value)
