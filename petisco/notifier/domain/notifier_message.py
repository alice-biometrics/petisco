from abc import abstractmethod

from dataclasses import dataclass


@dataclass
class NotifierMessage:
    message: str = None

    @abstractmethod
    def __str__(self) -> str:
        return self.message
