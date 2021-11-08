def apm_inject_in_custom_context(key: str, value: str):
    import elasticapm  # noqa

    elasticapm.set_custom_context({key: value})
