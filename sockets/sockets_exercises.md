# Sockets exercises

## Class exercises

1. Create a new file `sockets_server.py` where the simple server is modified so that the transport protocol used is changed to UDP (hint: `socket.SOCK_DGRAM`. Remove all connection-oriented calls). Only messages with a first byte equals to 1  will be now accepted. The reply will have the value 2 in the first byte.
2. Create a new file `sockets_client.py` where the client is adapted accordingly.
3. Modify the file `sockets_server.py` to define a message header with the following fields
    - Type of message (1 byte): can be integer (1), string (2), floating point (3), error code (4)
    - Size of payload (4 bytes): Size of the payload in bytes (integer will be 4 bytes, string maximum 256 bytes, floating point 8 bytes)
    - Error code will be an ASCII string with either the value "OK" or "ERROR - error description"
        - The server will catch type mismatch errors like, for instance, sending integers with more than 4 bytes or strings longer than the maximum length.
    - That is, the server will just send a reply of type error code (4) with either "OK" or "ERROR - error description". The client does not send messages of type error code to the server.
4. The client will now be able to send one of the three different types as payload and handle the error code. Adapt the client program accordingly.
    - The client program can accept an additional parameter from the command line indicating the type of the data to send to the server.
    - To keep things simple, the client will just output the reply from the server on the command line.


