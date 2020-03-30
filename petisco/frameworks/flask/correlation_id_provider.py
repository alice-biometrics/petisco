from petisco.domain.value_objects.correlation_id import CorrelationId


def flask_correlation_id_provider(func_name: str = "") -> CorrelationId:
    try:
        import connexion

        correlation_id_str = connexion.request.headers.get("X-Correlation-Id")
        if correlation_id_str:
            correlation_id = CorrelationId(correlation_id_str)
        else:
            correlation_id = CorrelationId.generate(func_name)
    except (RuntimeError, ImportError):
        correlation_id = CorrelationId.generate(func_name)
    return correlation_id
