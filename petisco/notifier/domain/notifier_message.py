from dataclasses import dataclass


@dataclass
class NotifierMessage:
    message: str = None
