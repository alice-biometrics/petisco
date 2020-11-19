import json


class WebhookRequestResult:
    @staticmethod
    def from_dict(kdict: dict):
        return WebhookRequestResult(
            headers=json.loads(kdict.get("headers")) if kdict.get("headers") else None,
            body=json.loads(kdict.get("body")) if kdict.get("body") else None,
        )

    def to_dict(self):
        return {
            "headers": json.dumps(self.headers) if self.headers else None,
            "body": json.dumps(self.body) if self.body else None,
        }

    def __init__(self, headers: dict, body: dict):
        self._set_headers(headers)
        self._set_body(body)
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
