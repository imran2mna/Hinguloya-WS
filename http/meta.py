class HttpHeader:
    USER_AGENT = "User-Agent"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT = "Accept"
    CONNECTION = "Connection"
    CACHE_CONTROL = "Cache-Control"

    SERVER = "Server"
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"

    def __init__(self):
        pass


class HTTP:
    VERSION_1_0 = 1.0
    VERSION_1_1 = 1.1

    VERSION_MAP = {
        VERSION_1_0: "HTTP/1.0",
        VERSION_1_1: "HTTP/1.1"
    }

    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500

    STATUS_MAP = {
        OK: "OK",
        BAD_REQUEST: "Bad Request",
        NOT_FOUND: "Not Found",
        SERVER_ERROR: "Internal Server Error"
    }

    def __init__(self):
        pass

    @staticmethod
    def get_status(status, version=1.1):
        return "{} {} {} ".format(HTTP.VERSION_MAP.get(version), str(status), HTTP.STATUS_MAP.get(status))


class TAGS:
    BODY_SEPARATOR = "\n\r\n"
    LINE_SEPARATOR = '\n'
    WHITE_SPACE = ' '
    HEADER_SEPARATOR = "\r"
    HEADER_KEY_SEPARATOR = ":"
    EMPTY_CHARACTER = ""

    URL_ROOT = "/"

    def __init__(self):
        pass
