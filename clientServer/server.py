# -*- coding: utf-8 -*-
import socket
import threading
import pickle
from _thread import *
import store.codes as codes
import utils.map as maps


EOF = '\0'
CRLF = '\r\n'

class Server(object):
    clients = []
    def __init__(self, mapa):
         self.mapa = mapa
         try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('127.0.0.1', 5655))
         except:
            print(codes.get_response_text(11))
         print('socket created')
    
    def recv_all(self, crlf, conn):
        data = ''
        while not data.endswith(crlf):
            data = data + conn.recv(1).decode()
        return data
    
    def run(self): 
        self.s.listen(4) 
        try:
            self.accept_clients()
        except Exception as ex:
            print(codes.get_response_text(11), ex)
        finally:
            for client in self.clients:
                client.close()
            self.s.close()
    
    def accept_clients(self):
        while True:
            (clientsocket, address) = self.s.accept()
            self.clients.append(clientsocket)
            #self.client_connected(clientsocket)
            start_new_thread(self.client_connected, (clientsocket,))

    def client_connected(self, client):
        print(' client connected: ', client)
        client.send(codes.get_code("Available").encode() + CRLF.encode())
        lvl = int(self.recv_all(CRLF, client))


        cards_map = mapa.create_map(lvl) # normal array
        # client.send(pickle.dumps(cards_map) + CRLF.encode())
        # print(' map sent')
            
        self.s.close()
            
if __name__ == '__main__':
    mapa = maps.Map()
    server = Server(mapa)
    server.run()
