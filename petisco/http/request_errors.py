from meiga import Error


class MultipartFormatRequestError(Error):
    error_name = str(__name__)
    error_message = {"error": "Fail to create multipart"}


class MissingSchemaRequestError(Error):
    error_name = str(__name__)
    error_message = {"error": "Missing schema in request"}


class TimeoutRequestError(Error):
    error_name = str(__name__)
    error_message = {"error": "Timeout error"}


class ConnectionRequestError(Error):
    error_name = str(__name__)
    error_message = {"error": "Connection error"}


class UnknownRequestError(Error):
    error_name = str(__name__)
    error_message = {"error": "General connection error"}
