from petisco.extra.elastic_apm.is_elastic_apm_available import is_elastic_apm_available


def capture_exception() -> None:
    if is_elastic_apm_available():
        import elasticapm  # noqa

        client = elasticapm.get_client()
        if client:
            client.capture_exception()
