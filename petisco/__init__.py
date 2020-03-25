import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

__version__ = open(f"{ROOT_PATH}/VERSION", "r").read()[:-1]

from petisco.public_api import *
from petisco import public_api

__all__ = public_api.__all__
