#!/usr/bin/env python
# encoding: utf8
#
# Copyright © Ruben Ruiz Torrubiano <ruben.ruiz at fh-krems dot ac dot at>,
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#---------------------------------------------------------
# GROUP MEMBERS: Alexander Savov and Balazs Csaba Madarasi
#---------------------------------------------------------

# Needed imports
from http.server import BaseHTTPRequestHandler, HTTPServer


# Define a custom HTTP server class which inherits from BaseHTTPRequestHandler class
class CustomHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Handling of GET requests
        :return:
        """
        # Check the requested path
        if self.path == '/example':
            # If the path is '/example', serve example.html
            with open('example.html', 'rb') as file:  # Open the HTML file in binary read mode
                self.send_response(200)  # Send a 200 OK response
                self.send_header('Content-type', 'text/html')  # Set the content type as HTML
                self.end_headers()  # End the HTTP headers
                self.wfile.write(file.read())  # Write the content of the file to the response

        # If the path is not '/example'
        else:
            try:
                page = open(self.path[1:], 'rb')  # Try to open the requested file by removing the leading '/'
                self.send_response(200)  # Send a 200 OK response
                self.send_header('Content-type', 'text/html')  # Set the content type as HTML
                self.end_headers()  # End the HTTP headers
                self.wfile.write(page.read())  # Write the content of the file to the response

            except OSError:
                # If the file is not found, send a 404 Not Found response
                self.send_error(404, 'Not found')


# Entry point of the script
if __name__ == "__main__":
    # Create an instance of HTTPServer listening on localhost 127.0.0.1 and port 80
    ws = HTTPServer(("127.0.0.1", 80), CustomHttpServer)
    print("Started server on port 80")  # Print a message indicating that the server has started

    try:
        ws.serve_forever()  # Start serving requests indefinitely
    except KeyboardInterrupt:
        pass  # Handle KeyboardInterrupt (Ctrl+C) to stop the server

    ws.server_close()  # Close the server when done
