from petisco import Event, UserId, ClientId, CorrelationId


class UserCreated(Event):
    user_id: UserId
    client_id: ClientId
    event_version: str
    event_correlation_id: CorrelationId = None

    def __init__(
        self,
        user_id: UserId,
        client_id: ClientId,
        correlation_id: CorrelationId,
        version: str = "1.0.0",
    ):
        self.user_id = user_id
        self.client_id = client_id
        self.correlation_id = correlation_id
        self.version = version
        super().__init__()
