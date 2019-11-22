from typing import Dict, Callable

from fakeredis import FakeRedis
from redis import Redis

from petisco.events.event import Event
from petisco.events.interface_event_manager import IEventManager


class FakeRedisBasedEventManager(IEventManager):
    def __init__(
        self, redis: Redis = FakeRedis(), subscribers: Dict[str, Callable] = None
    ):
        super().__init__(subscribers)
        self._redis = redis
        self._pubsub = self._redis.pubsub()
        self._subscribe()

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def _subscribe(self):
        self._pubsub.subscribe(**self.subscribers)

    def unsubscribe_all(self):
        pass

    def send(self, topic: str, event: Event):
        self._redis.publish(topic, event.to_json())
