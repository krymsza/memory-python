# -*- coding: utf-8 -*-

import socket
import store.codes as codes
import components.app as app

EOF = '\0'
CRLF = '\r\n'

class client:
    def __init__(self):
        
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print(codes.get_response_text(11))
        print('socket created')
            
    def recv_all(self, crlf):
        data = ''
        while not data.endswith(crlf):
            data = data + self.s.recv(1).decode()
        return data
    
    def get_response(self):
         response = self.recv_all(CRLF)
         print(codes.get_response_text(response))
         return int(response)
            
    def start(self):
        try:
            self.s.connect(('127.0.0.1', 5655))
            data = self.recv_all(CRLF)
            print('connented: ', codes.get_response_text(data))
        except:
            print(codes.get_response_text(11))
            
        app.get_layout(self.s)

        
if __name__ == '__main__':
    client = client()
    client.start()
    