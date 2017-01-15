import socket
import thread
from http import handler
import threading


class HTTPServer(threading.Thread):

    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        server_addr = (self.ip, self.port)
        server_socket = self.tcp_socket()
        try:
            server_socket.bind(server_addr)
            server_socket.listen(5)
        except socket.error, e:
            if e.errno == 98:
                print "Address already in use"
                exit(1)

        print "listening on ", self.port

        while True:
            thread.start_new_thread(handler.process_request, server_socket.accept())

    def tcp_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


threads = []
for i in [8090, 8091]:
    server_thread = HTTPServer('127.0.0.1', i)
    server_thread.start()
    threads.append(server_thread)

for i in threads:
    i.join()
