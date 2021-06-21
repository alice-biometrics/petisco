# from pika import BasicProperties
# from pika.exceptions import ChannelClosedByBroker
#
# from petisco.base.domain.message.domain_event import DomainEvent
# from petisco.base.domain.message.message_bus import MessageBus
# from petisco.extra.rabbitmq import RabbitMqMessageConfigurer
# from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_consumer_connector import RabbitMqConsumerConnector
# from petisco.extra.rabbitmq.application.message.formatter.rabbitmq_message_queue_name_formatter import \
#     RabbitMqMessageQueueNameFormatter
#
#
#
# class RabbitMqConsumerDomainEventBus(MessageBus):
#     def __init__(
#         self, connector: RabbitMqConsumerConnector, organization: str, service: str
#     ):
#         self.connector = connector
#         self.exchange_name = f"{organization}.{service}"
#         self.rabbitmq_key = f"publisher-{self.exchange_name}"
#         self.configurer = RabbitMqMessageConfigurer(connector, organization, service)
#         self.properties = BasicProperties(delivery_mode=2)  # PERSISTENT_TEXT_PLAIN
#
#     def publish(self, domain_event: DomainEvent):
#         if hasattr(self, "info_id"):
#             event = event.add_info_id(self.info_id)
#
#         if not event or not issubclass(event.__class__, Event):
#             raise TypeError("Bus only publishes petisco.Event objects")
#
#         try:
#             channel = self.connector.get_channel(self.rabbitmq_key)
#             routing_key = RabbitMqMessageQueueNameFormatter.format(
#                 event, exchange_name=self.exchange_name
#             )
#
#             channel.basic_publish(
#                 exchange=self.exchange_name,
#                 routing_key=routing_key,
#                 body=event.to_json(),
#                 properties=self.properties,
#             )
#         except ChannelClosedByBroker:
#             # If Event queue is not configured, it will be configured and publication retried.
#             self.configurer.configure_event(event)
#             self.publish(event)
#
#     def retry_publish_only_on_store_queue(self, event: Event):
#         if not event or not issubclass(event.__class__, Event):
#             raise TypeError("Bus only publishes petisco.Event objects")
#         channel = self.connector.get_channel(self.rabbitmq_key)
#         channel.basic_publish(
#             exchange=self.exchange_name,
#             routing_key="retry.store",
#             body=event.to_json(),
#             properties=self.properties,
#         )
#
#     def close(self):
#         self.connector.close(self.rabbitmq_key)
