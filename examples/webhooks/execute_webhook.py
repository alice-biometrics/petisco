from petisco import Webhook

SECRET = b"petiso-is-not-ready-for-production"
ORGANIZATION = "Petisco"

webhook = Webhook(
    post_url="http://127.0.0.1:5000/webhook",
    api_key="'b0b905d6-228f-44bf-a130-c85d7aecd765",
    secret=SECRET,
    organization=ORGANIZATION,
    event_name="user_created",
    event_version="1",
)

result = webhook.ping()
print(result)

result = webhook.execute({"user": "created"})
print(result)
