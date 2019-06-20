# -*- coding: utf-8 -*-

import socket
import logging
import store.codes as codes
import components.app as app

EOF = '\0'
CRLF = '\r\n'

class client:
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            logger.error('server internal error %s', codes.get_response_text(11))
            
    def recv_all(self, crlf):
        data = ''
        while not data.endswith(crlf):
            data = data + self.s.recv(1).decode()
        return data
    
    def get_response(self):
         response = self.recv_all(CRLF)
         logger.info(' %s ', codes.get_response_text(response))
         return int(response)
            
    def start(self):
        logger.info('client socket created')
        try:
            self.s.connect(('127.0.0.1', 5655))
            data = self.recv_all(CRLF)
            logger.info('connented: %s', codes.get_response_text(data))
            logger.info('Client started')
        except:
            logger.error(' %s', codes.get_response_text(11))
            
        app.get_layout(self.s)


if __name__ == '__main__':
    
    logger = logging.getLogger('client_logger')
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler('client.log')
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)

    client = client()
    client.start()
    