import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

with open(f"{ROOT_PATH}/VERSION") as f:
    __version__ = f.read().rstrip()

from petisco import public_api
from petisco.public_api import *

__all__ = public_api.__all__
