# -*- coding: utf-8 -*-
import socket 
import codes
import socketServer


EOF = '\0'
CRLF = '\r\n'

class Server(socketServer):
    def __init__(self):
        socketServer.__init__(self)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('127.0.0.1', 5655))
        except:
            print(codes.get_response_text(11))
   
    def recv_all(self, crlf):
        data = ""
        while not data.endswith(crlf):
            data = data + self.conn.recv(1).decode()
        return data
     
    def on_message(self, client, message):
        print('client message')

    def on_open(self, client):
        print('client connected')

    def on_close(self, client):
        print('client disconnected')
        


if __name__ == '__main__':
    server = Server()
    server.run()
