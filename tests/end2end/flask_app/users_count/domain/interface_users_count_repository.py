from typing import Dict

from meiga import Result, Error, NotImplementedMethodError

from petisco.application.interface_repository import IRepository


class IUsersCountRepository(IRepository):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def increase(self) -> Result[bool, Error]:
        return NotImplementedMethodError

    def decrease(self) -> Result[bool, Error]:
        return NotImplementedMethodError

    def count(self) -> Result[int, Error]:
        return NotImplementedMethodError
