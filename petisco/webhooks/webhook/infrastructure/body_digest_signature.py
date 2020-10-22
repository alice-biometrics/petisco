import hmac
import hashlib


class BodyDigestSignature(object):
    def __init__(self, secret, header="Sign", algorithm=hashlib.sha512):
        self.secret = secret
        self.header = header
        self.algorithm = algorithm

    def __call__(self, request):
        body = request.body
        if not isinstance(body, bytes):  # Python 3
            body = body.encode("latin1")  # standard encoding for HTTP
        signature = hmac.new(self.secret, body, digestmod=self.algorithm)
        request.headers[self.header] = signature.hexdigest()
        return request
