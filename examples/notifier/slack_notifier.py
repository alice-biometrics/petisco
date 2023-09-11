import os
import sys
import traceback

from petisco import NotifierExceptionMessage, NotifierMessage
from petisco.extra.slack import (
    BlocksSlackNotifierMessageConverter,
    ExceptionBlocksSlackNotifierMessageConverter,
    SlackNotifier,
)

token = os.getenv("SLACK_API_TOKEN")

if not token:
    raise ValueError("Please, configure the SLACK_API_TOKEN envvar")

gke_accessory = {
    "type": "button",
    "text": {"type": "plain_text", "text": "Code", "emoji": True},
    "value": "click_me_code",
    "url": "https://github.com/alice-biometrics/petisco",
    "action_id": "button-code",
    "style": "primary",
}
notifier = SlackNotifier(
    token=token,
    channel="warnings-staging",
    converter=BlocksSlackNotifierMessageConverter(slack_accessory=gke_accessory),
    exception_converter=ExceptionBlocksSlackNotifierMessageConverter(
        slack_accessory=gke_accessory,
        repository_url="https://github.com/alice-biometrics/petisco/blob/main",
        repository_name_button="Github :github:",
    ),
)
meta = {"version": "2.0.0", "petisco": "1.0.0b", "environment": "staging"}


def notify():
    notifier_message = NotifierMessage(title=":rocket: petisco is deployed", meta=meta)
    notifier.publish(notifier_message)


def notify_exception():
    def _notify_exceptuon(exception):
        _, _, tb = sys.exc_info()
        tb = traceback.extract_tb(tb)[-1]
        filename = tb.filename if tb and hasattr(tb, "filename") else None
        lineno = tb.lineno if tb and hasattr(tb, "lineno") else None

        notifier_exception_message = NotifierExceptionMessage(
            title=":man-shrugging::skin-tone-6: uncontrolled exception",
            executor="MyUseCase",
            exception=exception,
            traceback=traceback.format_exc(),
            filename=filename,
            lineno=lineno,
            input_parameters={"arg1": 2},
            meta=meta,
        )
        notifier.publish_exception(notifier_exception_message)

    try:
        print(1 / 0)
    except Exception as exception:
        _notify_exceptuon(exception)


notify()
notify_exception()
