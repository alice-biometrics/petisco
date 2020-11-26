from meiga import Success, Failure

from petisco import WebhookResultId, Response, TimeoutRequestError
from petisco.webhooks.webhook.domain.webhook_result import WebhookResult
from tests.modules.webook.mothers.webhook_mother import WebhookMother


class WebhookResultMother:
    @staticmethod
    def success():
        return WebhookResult.from_dict(
            {
                "webhook_result_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "webhook_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "sent_on": "2020-11-18 11:38:37.156162",
                "response": {
                    "headers": None,
                    "body": "",
                    "status_code": 200,
                    "completed_in_ms": 10,
                },
                "request": {
                    "headers": '{"X-Petisco-Event": "user_created", "X-Petisco-Event-Version": "1", "X-Petisco-Delivery": "a026531a-8512-4599-9491-81909ea8e31b", "X-Petisco-WebhookId": "1baa14dc-bda9-400f-b45b-428f26532f1d", "X-Petisco-Request-Timestamp": "2020-11-18 11:38:37.156162", "User-Agent": "Petisco-Hookshoot/", "apikey": "\'b0b905d6-228f-44bf-a130-c85d7aecd765"}',
                    "body": '{"payload": "ok"}',
                },
                "is_success": True,
            }
        )

    @staticmethod
    def success_from_create():
        webhook_result = WebhookResultMother.success()
        return WebhookResult.create(
            webhook=WebhookMother.default(),
            webhook_result_id=WebhookResultId.generate(),
            sent_on=webhook_result.sent_on,
            request_headers={
                "X-Petisco-Event": "user_created",
                "X-Petisco-Event-Version": "1",
                "X-Petisco-Delivery": "a026531a-8512-4599-9491-81909ea8e31b",
                "X-Petisco-WebhookId": "1baa14dc-bda9-400f-b45b-428f26532f1d",
                "X-Petisco-Request-Timestamp": "2020-11-18 11:38:37.156162",
                "User-Agent": "Petisco-Hookshoot/",
                "apikey": "'b0b905d6-228f-44bf-a130-c85d7aecd765",
            },
            request_body={"payload": "ok"},
            result=Success(Response(200)),
        )

    @staticmethod
    def failure_from_create():
        webhook_result = WebhookResultMother.success()
        return WebhookResult.create(
            webhook=WebhookMother.default(),
            webhook_result_id=WebhookResultId.generate(),
            sent_on=webhook_result.sent_on,
            request_headers={
                "X-Petisco-Event": "user_created",
                "X-Petisco-Event-Version": "1",
                "X-Petisco-Delivery": "a026531a-8512-4599-9491-81909ea8e31b",
                "X-Petisco-WebhookId": "1baa14dc-bda9-400f-b45b-428f26532f1d",
                "X-Petisco-Request-Timestamp": "2020-11-18 11:38:37.156162",
                "User-Agent": "Petisco-Hookshoot/",
                "apikey": "'b0b905d6-228f-44bf-a130-c85d7aecd765",
            },
            request_body={"payload": "ok"},
            result=Failure(TimeoutRequestError()),
        )

    @staticmethod
    def failure():
        return WebhookResult.from_dict(
            {
                "webhook_result_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "webhook_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "sent_on": "2020-11-18 11:41:18.140811",
                "response": {"headers": None, "body": None, "status_code": 503},
                "request": {
                    "headers": '{"X-Petisco-Event": "user_created", "X-Petisco-Event-Version": "1", "X-Petisco-Delivery": "14ac35e8-0483-40b2-b308-104309b7407b", "X-Petisco-WebhookId": "8d5dc972-a6c8-4c87-8f81-a4cb61dcb6a3", "X-Petisco-Request-Timestamp": "2020-11-18 11:41:18.140811", "User-Agent": "Petisco-Hookshoot/", "apikey": "\'b0b905d6-228f-44bf-a130-c85d7aecd765"}',
                    "body": '{"payload": "ok"}',
                },
                "is_success": False,
            }
        )

    @staticmethod
    def without_response():
        return WebhookResult.from_dict(
            {
                "webhook_result_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "webhook_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "sent_on": "2020-11-18 11:38:37.156162",
                "response": None,
                "request": {
                    "headers": '{"X-Petisco-Event": "user_created", "X-Petisco-Event-Version": "1", "X-Petisco-Delivery": "a026531a-8512-4599-9491-81909ea8e31b", "X-Petisco-WebhookId": "1baa14dc-bda9-400f-b45b-428f26532f1d", "X-Petisco-Request-Timestamp": "2020-11-18 11:38:37.156162", "User-Agent": "Petisco-Hookshoot/", "apikey": "\'b0b905d6-228f-44bf-a130-c85d7aecd765"}',
                    "body": '{"payload": "ok"}',
                },
                "is_success": True,
            }
        )

    @staticmethod
    def without_request():
        return WebhookResult.from_dict(
            {
                "webhook_result_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "webhook_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "sent_on": "2020-11-18 11:38:37.156162",
                "response": {
                    "headers": None,
                    "body": "",
                    "status_code": 200,
                    "completed_in_ms": 10,
                },
                "request": None,
                "is_success": True,
            }
        )

    @staticmethod
    def without_request_headers():
        return WebhookResult.from_dict(
            {
                "webhook_result_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "webhook_id": "a026531a-8512-4599-9491-81909ea8e31b",
                "sent_on": "2020-11-18 11:38:37.156162",
                "response": {
                    "headers": None,
                    "body": "",
                    "status_code": 200,
                    "completed_in_ms": 10,
                },
                "request": {"headers": None, "body": '{"payload": "ok"}'},
                "is_success": True,
            }
        )
