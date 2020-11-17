from petisco import Webhook, WebhookSender, Secret

webhook = Webhook.create(
    active=True,
    post_url="http://127.0.0.1:5000/webhook",
    api_key="'b0b905d6-228f-44bf-a130-c85d7aecd765",
    secret=Secret("00480065006C006C006F0020007700634222"),
    event_name="user_created",
    event_version="1",
)

ORGANIZATION = "Petisco"
sender = WebhookSender(organization=ORGANIZATION)

result = sender.ping(webhook)
print(result)

result = sender.execute(webhook, {"user": "created"})
print(result)
