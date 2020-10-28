import hashlib
import hmac
from functools import wraps

from flask import Flask, request, Response

app = Flask(__name__)


def verify_webhook_requests(f=None):
    """
    Verify the request signature of the request sent from Slack
    Generate a new hash using the app's signing secret and request data
    """

    SECRET = b"petiso-is-not-ready-for-production"

    @wraps(f)
    def wrapper(*args, **kwargs):
        signature = request.headers["X-Alice-Signature"]

        timestamp = request.headers["X-Alice-Request-Timestamp"]
        event_name = request.headers["X-Alice-Event"]
        event_version = request.headers["X-Alice-Event-Version"]
        data = request.data.decode("latin1")

        # e.g `1.user_created:2020-10-27 14:13:05.723716:b'{"user": "created"}'`
        format_req = str.encode(f"{event_name}.{event_version}:{timestamp}:{data}")

        request_hash = hmac.new(SECRET, format_req, hashlib.sha512).hexdigest()
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
