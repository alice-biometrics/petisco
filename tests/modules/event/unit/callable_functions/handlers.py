from meiga import BoolResult

from petisco import Event


def send_mail_handler(event: Event) -> BoolResult:
    pass


def send_sms_handler(event: Event) -> BoolResult:
    pass


def event_store(event: Event) -> BoolResult:
    pass


def requeue_event(event: Event) -> BoolResult:
    pass
