from petisco import Webhook

webhook = Webhook(
    post_url="http://127.0.0.1:5000/webhook",
    api_key="'b0b905d6-228f-44bf-a130-c85d7aecd765",
    secret=b"petiso-is-not-ready-for-production",
    event_triggered="user_created",
    organization="ALiCE",
)

webhook.ping()

webhook.execute({"user": "created"})
