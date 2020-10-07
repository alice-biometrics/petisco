from meiga import BoolResult

from petisco import Event


def send_mail_on_user_created(event: Event) -> BoolResult:
    pass


def send_referral_on_user_created(event: Event) -> BoolResult:
    pass


def send_promotion_on_user_created(event: Event) -> BoolResult:
    pass


def event_store(event: Event) -> BoolResult:
    pass


def requeue_event(event: Event) -> BoolResult:
    pass
