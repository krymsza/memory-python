# -*- coding: utf-8 -*-

import socket
import ssl
import logging
import store.codes as codes
import components.app as app

EOF = '\0'
CRLF = '\r\n'

class client:
    def __init__(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssl_conn = ssl.wrap_socket(self.s,
                                            cert_reqs=ssl.CERT_REQUIRED, 
                                            ssl_version=ssl.PROTOCOL_TLSv1_2,
                                            ca_certs="../../keys/trusted_certs.crt"
                                            )
            logger.info('encrypted socket created')
        except:
            logger.error('#0 server internal error %s', codes.get_response_text(11))
            
    def recv_all(self, crlf):
        data = ''
        try:
            while not data.endswith(crlf):
                data = data + self.ssl_conn.recv(1).decode()
        except:
             logger.warrning('Connection with server droped')    
        return data
    
    def get_response(self):
         try:
             response = self.recv_all(CRLF)
         except:
             logger.warning('Connection with server droped')
         logger.info(' %s ', codes.get_response_text(response))
         return int(response)
    
    def send_message(self, message, crlf):
        try:
            if type(message) == str:
                message = message.encode()
            self.ssl_conn.send(message + crlf.encode())
        except:
            logger.error('#1 %s , %s',codes.get_code("ServerError"),
                         codes.get_response_text(
                                 codes.get_code("ServerError")))
            return False
        return True
            
    def start(self):
        logger.info('client socket created')
        try:
            self.ssl_conn.connect(('127.0.0.1', 5655))
            cert = self.ssl_conn.getpeercert()
            
            if not cert or ssl.match_hostname(cert, "server"):
                raise Exception("Invalid SSL cert.")
            logger.info("Server certificate OK.")
            
            data = self.recv_all(CRLF) # avaible 
            if( int(data) == 10):
                logger.info('connented: %s', codes.get_response_text(data))
                logger.info('Client started')
                app.get_layout(self, self.ssl_conn)
            else:
                logger.error('#4: %s', codes.get_response_text(11))
        except:
            pass

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
    