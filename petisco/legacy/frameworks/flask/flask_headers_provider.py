def flask_headers_provider() -> dict:
    try:
        import connexion

        headers = connexion.request.headers
        headers = {h: v for h, v in headers.items() if isinstance(h, str)}
    except (RuntimeError, ImportError):
        headers = {}

    return headers
