import json

from meiga import Result


class WebhookResponseResult:
    @staticmethod
    def from_result(result: Result):
        if result.is_success:
            response = result.unwrap()
            return WebhookResponseResult(
                headers=response.headers,
                body=response.content,
                status_code=response.status_code,
            )

        error = result.value
        return WebhookResponseResult(
            headers=error.headers, body=error.content, status_code=error.status_code
        )

    @staticmethod
    def from_dict(kdict: dict):
        return WebhookResponseResult(
            headers=json.loads(kdict.get("headers")) if kdict.get("headers") else None,
            body=kdict.get("body"),
            status_code=kdict.get("status_code"),
        )

    def to_dict(self):
        return {
            "headers": json.dumps(self.headers) if self.headers else None,
            "body": self.body,
            "status_code": self.status_code,
        }

    def __init__(self, headers: dict, body: dict, status_code: int):
        self.headers = headers
        self.body = body
        self.status_code = status_code
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
