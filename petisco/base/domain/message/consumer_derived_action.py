from typing import Dict

from pydantic.main import BaseModel


class ConsumerDerivedAction(BaseModel):
    action: str = None
    exchange_name: str = None
    routing_key: str = None
    headers: Dict = None
    # def __init__(
    #     self,
    #     action: str = None,
    #     exchange_name: str = None,
    #     routing_key: str = None,
    #     headers: Dict = None,
    # ):
    #     self.action = action
    #     self.exchange_name = exchange_name
    #     self.routing_key = routing_key
    #     self.headers = headers
    #
    # def to_dict(self):
    #     if not self.action:
    #         return {}
    #     else:
    #         return {
    #             "action": self.action,
    #             "exchange_name": self.exchange_name,
    #             "routing_key": self.routing_key,
    #             "headers": self.headers,
    #         }
