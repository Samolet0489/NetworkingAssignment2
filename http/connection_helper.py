#!/usr/bin/env python3
# This module defines general functions for establishing an arbitrary TCP connection with a remote host

#---------------------------------------------------------
# GROUP MEMBERS: Alexander Savov and Balazs Csaba Madarasi
#---------------------------------------------------------

# Needed imports
import socket
import ssl


# Defining a function to create a connection
def create_connection(address):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    conn.connect(address)  # Connect to the specified address (host, port)
    return conn  # Return this connection


# Defining a class which helps to establish a TCP connection
class HttpConnectionHelper:
    """
    Helper class for establishing a TCP connection
    """

    def __init__(self):  # Defining the constructor
        """
        Constructor
        """
        self.internal_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect method of the class
    # The port is 80 if it is not secure --> might be changed in line 36-38
    def connect(self, host, port=80, secure=False):
        """
        Establishes a connection
        :return:
        """
        # Determine the connection port based on security (HTTP or HTTPS)
        connection_port = port
        if secure:
            connection_port = 443

        # Connect to the server using the specified host and port
        self.internal_connection.connect((host, connection_port))

        # If secure (HTTPS), wrap the socket with SSL/TLS encryption
        if secure:
            self.internal_connection = ssl.wrap_socket(self.internal_connection, keyfile=None, certfile=None,
                                                       server_side=False, cert_reqs=ssl.CERT_NONE,
                                                       ssl_version=ssl.PROTOCOL_SSLv23)

    # Defining a method to send requests
    def send_request(self, request):
        """
        Sends an arbitrary request
        :param request: The request to send (as text)
        :return:
        """
        # Encode and send the HTTP request
        self.internal_connection.send(request.encode())

    # Defining a method to receive responses
    def receive_response(self):
        """
        Waits and receives a response form the server
        :return:
        """
        # Wait to receive the response --> up to 4096 bytes
        return repr(self.internal_connection.recv(4096))

    # Defining a method to close the connection
    def close(self):
        """
        Closes the connection
        :return:
        """
        # Close the TCP connection
        self.internal_connection.close()


# Entry point of the script
if __name__ == "__main__":
    # Create an instance of HttpConnectionHelper
    connection_helper = HttpConnectionHelper()

    # Establish a secure HTTPS connection to www.google.at on port 443
    connection_helper.connect("www.google.at", 443, True)

    # Send an HTTP HEAD request to the server
    connection_helper.send_request("HEAD / HTTP/1.1\r\nHost: www.google.at\r\n\r\n")

    # Receive the HTTP response from the server
    response = connection_helper.receive_response()

    # Print the HTTP response headers
    http_response_headers = repr(response)
    print(http_response_headers)
