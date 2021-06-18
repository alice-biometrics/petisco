from typing import Dict

from petisco import Uuid


class MessageMetaMother:
    @staticmethod
    def with_meta_with_info() -> Dict:
        return {
            "info_id": {
                "client_id": "petisco-client",
                "user_id": Uuid.v4().value,
                "correlation_id": Uuid.v4().value,
            }
        }
