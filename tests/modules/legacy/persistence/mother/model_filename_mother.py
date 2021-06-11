import os

BASE_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../ymls/"


class ModelFilenameMother:
    @staticmethod
    def get(suffix: str):
        return f"{BASE_PATH}/{suffix}"
