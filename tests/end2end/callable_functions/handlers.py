from meiga import Result, Error

from petisco import Event


def send_mail_on_user_created(event: Event) -> Result[bool, Error]:
    pass


def send_referral_on_user_created(event: Event) -> Result[bool, Error]:
    pass


def send_promotion_on_user_created(event: Event) -> Result[bool, Error]:
    pass
