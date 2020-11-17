import hashlib
import hmac
from functools import wraps

from flask import Flask, request, Response

from petisco import Secret

app = Flask(__name__)


def verify_webhook_requests(f=None):
    """
    Verify the request signature of the request sent from Slack
    Generate a new hash using the app's signing secret and request data
    """

    secret = Secret("00480065006C006C006F0020007700634222")
    ORGANIZATION = "Petisco"

    @wraps(f)
    def wrapper(*args, **kwargs):
        signature = request.headers[f"X-{ORGANIZATION}-Signature"]

        timestamp = request.headers[f"X-{ORGANIZATION}-Request-Timestamp"]
        event_name = request.headers[f"X-{ORGANIZATION}-Event"]
        event_version = request.headers[f"X-{ORGANIZATION}-Event-Version"]
        data = request.data.decode("latin1")

        # e.g `user_created.1:2020-10-28 07:33:37.243390:{"is_ping": true}`
        format_req = str.encode(f"{event_name}.{event_version}:{timestamp}:{data}")
        print(format_req)
        request_hash = hmac.new(
            secret.get_bytes(), format_req, hashlib.sha1
        ).hexdigest()
        calculated_signature = request_hash
        if hmac.compare_digest(calculated_signature, signature):
            return f(*args, **kwargs)

        print(f"HMAC is not valid: {calculated_signature} is not {signature}")

        return Response(status=401)

    return wrapper


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return Response(status=200)


@app.route("/webhook", methods=["POST"])
@verify_webhook_requests
def webhook_receiver():
    print("-" * 100)
    print(f"headers:\n{request.headers}")
    print(f"payload: {request.data}")
    print("-" * 100)

    return Response(status=200)
