import json


class WebhookRequestResult:
    @staticmethod
    def from_dict(kdict: dict):
        return WebhookRequestResult(
            headers=json.loads(kdict.get("headers")) if kdict.get("headers") else None,
            body=kdict.get("body"),
        )

    def to_dict(self):
        return {
            "headers": json.dumps(self.headers) if self.headers else None,
            "body": self.body,
        }

    def __init__(self, headers: dict, body: dict):
        self.headers = headers
        self.body = body
        super().__init__()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False
