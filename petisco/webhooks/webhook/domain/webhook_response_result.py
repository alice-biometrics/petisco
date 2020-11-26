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
                completed_in_ms=response.completed_in_ms,
            )

        error = result.value
        return WebhookResponseResult(
            headers=error.headers,
            body=error.content,
            status_code=error.status_code,
            completed_in_ms=error.completed_in_ms,
        )

    @staticmethod
    def from_dict(kdict: dict):
        return WebhookResponseResult(
            headers=json.loads(kdict.get("headers")) if kdict.get("headers") else None,
            body=json.loads(kdict.get("body")) if kdict.get("body") else None,
            status_code=kdict.get("status_code"),
            completed_in_ms=kdict.get("completed_in_ms"),
        )

    def to_dict(self):
        return {
            "headers": json.dumps(self.headers) if self.headers else None,
            "body": json.dumps(self.body) if self.body else None,
            "status_code": self.status_code,
            "completed_in_ms": self.completed_in_ms,
        }

    def __init__(
        self, headers: dict, body: dict, status_code: int, completed_in_ms: float = None
    ):
        self._set_headers(headers)
        self._set_body(body)
        self.status_code = status_code
        self.completed_in_ms = completed_in_ms
        super().__init__()

    def _set_headers(self, headers):
        try:
            self.headers = dict(headers)
        except Exception:
            self.headers = {}

    def _set_body(self, body):
        try:
            self.body = dict(body)
        except Exception:
            self.body = {}

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False
