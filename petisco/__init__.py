import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

__version__ = open(f"{ROOT_PATH}/VERSION", "r").read().rstrip()

from petisco import public_api
from petisco.public_api import *

__all__ = public_api.__all__
