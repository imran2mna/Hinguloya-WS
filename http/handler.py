from file.content import ContentManager
from parser import ServerHttpRequest, ServerHttpResponse
from conf.basic import SUPRESS_EXCEPTION


def process_request((client_socket, addr), server):
    try:
        req_msg = read_socket(client_socket)

        http_req = ServerHttpRequest(req_msg)
        proto_version = http_req.get_proto_version()

        status, content = ContentManager(http_req.get_url(), server.get_doc_root()).read()

        http_res = ServerHttpResponse(status, content, proto_version)

        client_socket.send(http_res.generate_response())
    except Exception, e:
        if not SUPRESS_EXCEPTION:
            print e.message


def read_socket(input_socket):
    chunks = []
    size = 128
    buffer_size = 128

    while size == buffer_size:
        chunk = input_socket.recv(buffer_size)
        chunks.append(chunk)
        size = len(chunk)

    return ''.join(chunks)
