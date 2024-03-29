# -*- coding: utf-8 -*-
import socket
import random
import pickle
import store.options as options
from threading import Thread
import store.codes as codes
import utils.map as maps

EOF = '\0'
CRLF = '\r\n'

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

class Server():
     clients = []
     def __init__(self, mapa):
         self.mapa = mapa
         try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(('127.0.0.1', 5655))
         except:
            print(codes.get_response_text(11))
         print('Server running')
    
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
            print(' within for connections')
            (clientsocket, (ip, port)) = self.s.accept()
            t = Thread(target = ClientThread,args = (clientsocket, ip, port)).start()
            self.clients.append(t)
            print('domer')
            ''' for t in self.clients: 
                t.join() '''
            
         
         
class ClientThread(Thread):

    def __init__(self, client, ip, port):
        print(' init client thread')
        Thread.__init__(self)
        self.ip = ip 
        self.port = port
        self.set_game(client)
                 
    def recv_all(self, crlf, conn):
        data = ''
        while not data.endswith(crlf):
            data = data + conn.recv(1).decode()
        return data

    def recv_int(self, conn):
        res = conn.recv(10)
        return int_from_bytes(res)
    
    def recv_array(self, conn):
        data = conn.recv(1)
        while not data.endswith(CRLF.encode()):
            data += conn.recv(1)
        return pickle.loads(data)

    def set_game(self, client):
        client.send(codes.get_code("Available").encode() + CRLF.encode())
        level = int(self.recv_int(client))
        cards_map = mapa.create_map(level) # normal array
        random.shuffle(cards_map)
        for i in range (0, 6):
            print(cards_map[i].pos, " : ", cards_map[i].word)
        client.send(codes.get_code("Success").encode() + CRLF.encode())

        self.handle_game(client, cards_map, level)
    
    def handle_game(self, client, cards_map, level):
        self.card_sent = 0
        self.solved_pairs = 0
        while True:
            print('waiting for answer...')
            ans = self.recv_all(CRLF, client)
            client.send(cards_map[int(ans)].word.encode() + CRLF.encode()) 
            self.card_sent += 1
            if self.card_sent == 2:
                self.card_sent = 0
                cards_to_check = self.recv_array(client)
                
                if cards_map[cards_to_check[0]].word == cards_map[cards_to_check[1]].word:
                    self.solved_pairs += 1
                    if self.solved_pairs == options.levels[level]:
                        client.send(codes.get_code("GameOver").encode() + CRLF.encode())
                        next_game = int(self.recv_all(CRLF, client))
                        if next_game == int(codes.get_code("NewGame")):
                            #new game
                            self.set_game(client)
                            break
                        else:
                            #end program for client
                            self.endGame(client)
                            break
                    else:
                        client.send(codes.get_code("PairFound").encode() + CRLF.encode())
                else:
                    client.send(codes.get_code("PairNotFound").encode() + CRLF.encode())
                
                
        pass
    
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)
    
    def endGame(self, client):
        #self.clients.remove(client)
        #client.close()
        #Closing thread
        print('clients count: ', len(self.clients))
    
        
if __name__ == '__main__':
    mapa = maps.Map()
    server = Server(mapa)
    server.run()
