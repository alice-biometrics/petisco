def is_elastic_apm_available() -> bool:
    try:
        import elasticapm  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
