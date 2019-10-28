from petisco.controller.correlation_id import CorrelationId


def flask_correlation_id_provider(func_name: str = "") -> CorrelationId:
    try:
        import connexion
        correlation_id = CorrelationId(connexion.request.headers.get("X-Correlation-Id"))
    except ImportError:
        correlation_id = CorrelationId.generate(func_name)
    return correlation_id
