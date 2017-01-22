import socket
import thread
from http import handler
import threading
import tcp_socket


class HTTPServer(threading.Thread):

    def __init__(self, ip, port, document_root):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.document_root = document_root

    def get_doc_root(self):
        return self.document_root

    def run(self):
        server_addr = (self.ip, self.port)
        server_socket = tcp_socket.create_ipv4_server()
        try:
            server_socket.bind(server_addr)
            server_socket.listen(0)
        except socket.error, e:
            if e.errno == 98:
                print "Address already in use ( %s : %d )" % (self.ip, self.port)
                exit(1)

        print "server listening on ( %s : %d )" % (self.ip, self.port)

        while True:
            thread.start_new_thread(handler.process_request, (server_socket.accept(), self))


server = HTTPServer('127.0.0.1', 8080, '/home/imran/Desktop/')
server.start()