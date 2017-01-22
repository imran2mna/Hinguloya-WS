import socket


def create_ipv4_server():
    return create_ipvx_server(socket.AF_INET)


def create_ipv6_server():
    return create_ipvx_server(socket.AF_INET6)


def create_ipvx_server(ipvx):
    return socket.socket(ipvx, socket.SOCK_STREAM)