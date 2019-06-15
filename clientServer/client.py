# -*- coding: utf-8 -*-

import socket
import json
import pickle
import store.codes as codes

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
    
    '''def recv_map(self, crlf):
        data = ''.encode()
        while not data.endswith(crlf.encode()):
            recived = self.s.recv(100)
            data += recived
        return data'''
            
    def start(self):
        try:
            self.s.connect(('127.0.0.1', 5655))
            data = self.recv_all(CRLF)
            print('connented: ', codes.get_response_text(data))
        except:
            print(codes.get_response_text(11))
            
        self.s.send("2".encode() + CRLF.encode())
        self.get_response()
        # result = self.recv_map(CRLF)
        # result = pickle.loads(result)

if __name__ == '__main__':
    client = client()
    client.start()