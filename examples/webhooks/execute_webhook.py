from petisco.legacy import Webhook, WebhookSender, Secret, SignatureAlgorithm

webhook = Webhook.create(
    active=True,
    post_url="http://127.0.0.1:5000/webhook",
    api_key="'b0b905d6-228f-44bf-a130-c85d7aecd765",
    secret=Secret("9464a12f2186cdfe38fd1cfd797758c47c544e99"),
    event_name="user_created",
    event_version="1",
    algorithm=SignatureAlgorithm.sha512(),
)

ORGANIZATION = "Petisco"
sender = WebhookSender(organization=ORGANIZATION)

result = sender.ping(webhook)
print(result)

result = sender.execute(webhook, {"user": "created"})
print(result)
