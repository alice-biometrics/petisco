from petisco import Webhook, WebhookSender

webhook = Webhook.create(
    post_url="http://127.0.0.1:5000/webhook",
    api_key="'b0b905d6-228f-44bf-a130-c85d7aecd765",
    event_name="user_created",
    event_version="1",
)

SECRET = b"petiso-is-not-ready-for-production"
ORGANIZATION = "Petisco"
sender = WebhookSender(secret=SECRET, organization=ORGANIZATION)

result = sender.ping(webhook)
print(result)

result = sender.execute(webhook, {"user": "created"})
print(result)
