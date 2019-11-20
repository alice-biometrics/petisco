from typing import Dict, Callable
from redis import Redis

from petisco.events.event import Event
from petisco.events.interface_event_manager import IEventManager


class RedisBasedEventManager(IEventManager):
    def __init__(self, redis: Redis, subscribers: Dict[str, Callable]):
        super().__init__(subscribers)
        self._redis = redis
        self._pubsub = self._redis.pubsub()
        self._subscribe()

    def _subscribe(self):
        self._pubsub.subscribe(**self.subscribers)
        self._thread = self._pubsub.run_in_thread(sleep_time=0.001)

    def unsubscribe_all(self):
        self._thread.stop()

    def send(self, topic: str, event: Event):
        self._redis.publish(topic, event.to_json())
