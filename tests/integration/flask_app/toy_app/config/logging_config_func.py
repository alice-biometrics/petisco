import logging


def logging_config_func():
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("openapi_spec_validator").setLevel(logging.WARNING)
    logging.getLogger("connexion").setLevel(logging.WARNING)
    logging.getLogger("pika").setLevel(logging.WARNING)
