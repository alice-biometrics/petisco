import os

from petisco.notifier.infrastructure.slack.slack_notifier import SlackNotifier

token = os.environ["SLACK_API_TOKEN"]

notifier = SlackNotifier(token)

notifier.publish("hi")
