from conf.basic import SERVER_NAME
from meta import *


class ServerHttpRequest:

    def __init__(self, msg):
        # http request contains two parts - header, body
        request_structure = msg.split(TAGS.BODY_SEPARATOR)
        # extract header records
        headers = request_structure[0].split(TAGS.LINE_SEPARATOR)

        self.method = None
        self.location = None
        self.proto_version = HTTP.VERSION_1_1

        try:
            # first line describes HTTP 'GET / HTTP/1.0'
            proto_descriptors = headers[0].split(TAGS.WHITE_SPACE)
            self.method = proto_descriptors[0]
            self.location = proto_descriptors[1]
            self.proto_version = float(proto_descriptors[2].split(TAGS.URL_ROOT)[1])
        except IndexError, ie:
            # print ie.message
            print "Index error - ", msg

        self.user_agent = None
        self.accept_encoding = None
        self.accept_language = None
        self.accept = None

        # map each header record as per need
        for header in headers[1:]:
            header_desc = header.replace(TAGS.HEADER_SEPARATOR, TAGS.EMPTY_CHARACTER).split(TAGS.HEADER_KEY_SEPARATOR)
            self.map_header(header_desc[0], header_desc[1])

        # set request body
        self.body = None
        try:
            self.body = request_structure[1]
        except IndexError, e:
            print "request body not available"
            pass

    def get_method(self):
        return self.method

    def get_url(self):
        return self.location

    def get_proto_version(self):
        return self.proto_version

    def get_user_agent(self):
        return self.user_agent

    def map_header(self, key, value):

        if key is not None and value is not None:

            if key == HttpHeader.USER_AGENT:
                self.user_agent = value

            elif key == HttpHeader.ACCEPT_ENCODING:
                self.accept_encoding = value

            elif key == HttpHeader.ACCEPT_LANGUAGE:
                self.accept_language = value

            elif key == HttpHeader.ACCEPT:
                self.accept = value


class ServerHttpResponse:
    def __init__(self, status, content,  protocol=HTTP.VERSION_1_1, server_name=SERVER_NAME):
        self.protocol = protocol
        self.status = status
        self.content = content
        self.server_name = server_name

    def generate_response(self):
        # set http protocol, content-length
        http_proto = HTTP.get_status(self.status, self.protocol)
        content_length = len(self.content)

        header = ['%s : %s \r\n' % (HttpHeader.SERVER, SERVER_NAME),
                  '%s : %s \r\n' % (HttpHeader.CONTENT_TYPE, "text/html; charset=utf-8"),
                  '%s : %d \r\n' % (HttpHeader.CONTENT_LENGTH, content_length),
                  '%s : %s \r\n' % (HttpHeader.CONNECTION, "keep-alive")
                  ]

        response = '%s\n%s\r\n%s' % (http_proto, ''.join(header), self.content)

        return response
