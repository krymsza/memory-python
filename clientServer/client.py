# -*- coding: utf-8 -*-

import socket
import codes

EOF = '\0'
CRLF = '\r\n'

class client:
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print(codes.get_response_text(11))
            
    def start(self):
        try:
            self.s.connect(('127.0.0.1', 8080))
        except:
            print(codes.get_response_text(11))
            self.s.close()

if __name__ == '__main__':
    client = client()
    client.start()
    