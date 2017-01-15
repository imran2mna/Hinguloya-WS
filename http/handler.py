from file.content import ContentManager
from parser import ServerHttpRequest, ServerHttpResponse


def process_request(client_socket, addr):
    req_msg = read_socket(client_socket)
    # try:

    http_req = ServerHttpRequest(req_msg)
    proto_version = http_req.get_proto_version()

    status, content = ContentManager(http_req.get_url()).read()

    http_res = ServerHttpResponse(status, content, proto_version)

    client_socket.send(http_res.generate_response())

    # except Exception, e:
    #     msg = server_http_response.get_status(HTTPStatus.SERVER_ERROR)
    #     input_socket.send(msg)
    #     input_socket.send("server : PYTHON \r")
    #     input_socket.send("\n\r\n")
    #     input_socket.send("Internal Error")


def read_socket(input_socket):
    chunks = []
    size = 128
    buffer_size = 128

    while size == buffer_size:
        chunk = input_socket.recv(buffer_size)
        chunks.append(chunk)
        size = len(chunk)

    return ''.join(chunks)
