from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.value_objects.user_id import UserId


class InfoIdMother:
    @staticmethod
    def random():
        return InfoId(
            ClientId("petisco-client"), UserId.generate(), CorrelationId.generate()
        )
