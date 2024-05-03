#!/usr/bin/env python3
# This module defines general functions for establishing an arbitrary TCP connection with a remote host

import socket
import ssl


class HttpConnectionHelper:
    """
    Helper class for establishing a TCP connection
    """

    def __init__(self):
        """
        Constructor
        """
        self.internal_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port=80, secure=False):
        """
        Establishes a connection
        :return:
        """
        connection_port = port
        if secure:
            connection_port = 443
        self.internal_connection.connect((host, connection_port))
        if secure:
            self.internal_connection = ssl.wrap_socket(self.internal_connection, keyfile=None, certfile=None,
                                                       server_side=False, cert_reqs=ssl.CERT_NONE,
                                                       ssl_version=ssl.PROTOCOL_SSLv23)

    def send_request(self, request):
        """
        Sends an arbitrary request
        :param request: The request to send (as text)
        :return:
        """
        self.internal_connection.send(request.encode())

    def receive_response(self):
        """
        Waits and receives a response form the server
        :return:
        """
        return repr(self.internal_connection.recv(4096))

    def close(self):
        """
        Closes the connection
        :return:
        """
        self.internal_connection.close()


if __name__ == "__main__":
    connection_helper = HttpConnectionHelper()
    connection_helper.connect("www.google.at", 443, True)
    connection_helper.send_request("HEAD / HTTP/1.1\r\nHost: www.google.at\r\n\r\n")
    response = connection_helper.receive_response()
    http_response_headers = repr(response)
    print(http_response_headers)
