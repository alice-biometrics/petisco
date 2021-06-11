import hmac
import hashlib


class BodyDigestSignature(object):
    def __init__(self, secret, organization, header="Sign", algorithm=hashlib.sha1):
        self.secret = secret
        self.organization = organization
        self.header = header
        self.algorithm = algorithm

    def __call__(self, request):
        msg = self._format_message(request).encode("latin1")
        signature = hmac.new(key=self.secret, msg=msg, digestmod=self.algorithm)
        request.headers[self.header] = signature.hexdigest()
        return request

    def _format_message(self, request):
        event_name = request.headers.get(f"X-{self.organization}-Event")
        event_version = request.headers.get(f"X-{self.organization}-Event-Version")
        timestamp = request.headers.get(f"X-{self.organization}-Request-Timestamp")
        body = request.body

        return f"{event_name}.{event_version}:{timestamp}:{body}"
