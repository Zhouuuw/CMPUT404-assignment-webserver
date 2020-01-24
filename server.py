#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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

# source code should be cited: 
# https://github.com/python/cpython/blob/3.6/Lib/socketserver.py
# https://docs.python.org/3.6/library/socketserver.html#socketserver.BaseRequestHandler.handle
#

class Error404(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) 
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

class Error405(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) 
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

class Error301(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) 
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

# error raising reference:https://blog.csdn.net/skullFang/article/details/78820541

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        try:
            # Get HTTP method and url
            data_lst = self.data.decode("utf-8").split("\r\n")
            #print(data_lst)

            temp = data_lst[0].split(" ")
            #print(temp)
            if len(temp) != 3:
                raise Exception("HTTP request header invalid")
            self.method = temp[0]
            self.url = temp[1]
            self.version = temp[2]

            if self.method.upper()  != "GET":
                raise Error405("405 Method Not Allowed")

            else:
                if self.url[-5:] != '.html' and self.url[-4:] != ".css" and self.url[-1] != "/":
                    raise Error301("may need path ending")

                if self.url[-1] == "/":
                    self.url += "index.html"

                current_dict = os.getcwd()+"/www"
                file_path = current_dict + self.url
                #print(file_path)
                
                if not os.path.isfile(file_path) or not os.access(file_path,os.R_OK):
                    raise Error404("file not found")
                    #the file is not exist reference:
                    # https://docs.python.org/3.6/library/os.path.html 
                    # https://www.cnblogs.com/jhao/p/7243043.html  
                else:
                    filename,file_extension = os.path.splitext(file_path)
                    #print(file_extension)
                    if file_extension == ".html":
                        content = self.version + " 200 ok\r\nContent-Type: text/html\r\n\r\n"
                    elif file_extension == ".css":
                        content = self.version + " 200 ok\r\nContent-Type: text/css\r\n\r\n"
                    file = open(file_path)
                    content += file.read() 
                    file.close()
                    self.request.sendall(content.encode())
                    # reference about header files:
                    # https://www.runoob.com/http/http-header-fields.html
                    # https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Basics_of_HTTP/MIME_types

        except Error301 as e:
            response = self.version + " 301 Moved Permanently\r\nlocation:"+self.url+"/\r\nContent-Type: text/html\r\n\r\n"
            self.request.sendall(response.encode())

        except Error405 as e:
            response = self.version + " 405 Method Not Allowed\r\nContent-Type:text/html\r\n\r\n"
            self.request.sendall(response.encode())

        except Error404 as e:
            response = self.version + " 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
            self.request.sendall(response.encode())
        
        except Exception as e:
            print(e)

        #self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
