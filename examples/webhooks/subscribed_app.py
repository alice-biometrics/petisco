from flask import Flask, request, Response

app = Flask(__name__)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return Response(status=200)


@app.route("/webhook", methods=["POST"])
def webhook_receiver():
    print("-" * 100)
    print(f"headers:\n{request.headers}")
    print(f"payload: {request.json}")
    print("-" * 100)
    return Response(status=200)
