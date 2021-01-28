#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Zihao Huang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


def respond200(uri):

    root = "./www"

    if (uri[-1] == "/"):
        root += uri + "index.html"
    else: 
        root += uri
    path = uri.split("/")
    go_in = go_out = 0
    for each in path:
        if each == "..":
            go_out += 1
        if each != "..":
            go_in += 1

    if go_out > go_in:
        return respond404()
        
    try:
        body = open(root).read()
    except:
        return respond404()

    status = "HTTP/1.1 200 OK\r\n"
    if (uri[-1] == "/"):
        
        content_type = "Content-type: text/html;charset=utf-8\r\n"
    else:
        content_type = "Content-type: text/"+uri.split("/")[-1].split(".")[-1]+";charset=utf-8\r\n"
        
    content_length = "Content-Length: "+ str(len(body))+"\r\n\n"

    response = status + content_type + content_length + body

    return response

def respond301(uri):
    response = "HTTP/1.1 301 Moved Permanently\r\nLocation: "+uri +"/"+"\r\n\n"
    return response

def respond404():
    status = "HTTP/1.1 404 File not found\r\n"
    content_type = "Content-type: text/html;charset=utf-8\r\n"
    
    body = "<html><body><h1>404 PAGE NOT FOUND</h1></body></html>"
    content_length = "Content-Length: "+ str(len(body))+"\r\n\n"

    response = status + content_type + content_length + body
    return response

def respond405():

    status = "HTTP/1.1 405 Method Not Allowed\r\nAllow: GET, HEAD\r\n"
    content_type = "Content-type: text/html;charset=utf-8\r\n"
    
    body = "<html><body><h1>405 METHOD NOT ALLOWED</h1></body></html>"
    content_length = "Content-Length: "+ str(len(body))+"\r\n\n"

    response = status + content_type + content_length + body
    return response

def getResponse(request):
    if (request[0] == 'GET'):
        uri = request[1]
        path = "www"+uri+"/"
        if (uri[-1] != "/" and os.path.isdir(path)):
            return respond301(uri)
        
        return respond200(uri)

    else:
        return respond405()


class MyWebServer(socketserver.BaseRequestHandler):
    
    # def handle(self):
    #     self.data = self.request.recv(1024).strip()
    #     print ("Got a request of: %s\n" % self.data)
    #     self.request.sendall(bytearray("OK",'utf-8'))
    def handle(self):
        self.data = self.request.recv(1024).strip()
        raw_request = self.data.decode().split('\n')
        HTTPRequest = raw_request[0]

        request = (HTTPRequest.split()[0], HTTPRequest.split()[1])
        response = getResponse(request)
        self.request.sendall(response.encode())
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
