# -*- coding: utf-8 -*-
import socket
import ssl
import pickle
import logging
import store.options as options
from threading import Thread
import store.codes as codes
import utils.map as maps

EOF = '\0'
CRLF = '\r\n'

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

class Server(object):
     clients = []
     def __init__(self, mapa):
         self.mapa = mapa
         try:
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(('127.0.0.1', 5655))
         except:
            logger.error(' %s', codes.get_response_text(11))
         logger.info('Server started')
    
     def run(self): 
        self.s.listen(4)
        try:
            self.accept_clients()
        except Exception as ex:
            logger.error('%s, %s', codes.get_response_text(11), ex)
        finally:
            for client in self.clients:
                client.close()
            self.s.close()
    
     def accept_clients(self):
        while True:
            try:
                logger.info('waiting for connections...')
                logger.info('Server: %d players connected', len(self.clients))
                (clientsocket, (ip, port)) = self.s.accept()
                logger.info('%s: %d connected', ip, port)
                try:
                    #enctypted connection for client
                    ssl_client = ssl.wrap_socket(clientsocket, server_side=True, 
        					certfile="../../keys/server.cert", keyfile="../../keys/server.key", 
                            ssl_version=ssl.PROTOCOL_TLSv1_2)
                    #wrapped sock added
                    logger.info('Encrypted connection for %s started', ip)
                    t = Thread(target=ClientThread, args = (ssl_client, ip, port), daemon=True)
                    t.start()
                    self.clients.append(ssl_client)
                except ssl.SSLError:
                    pass
				
            except KeyboardInterrupt:
                self.s.close()
                logger.info("Finished.")

     @classmethod       
     def remove(self, client):
        self.clients.remove(client)
     
     @classmethod 
     def close_server(self):
         self.s.close()
         
class ClientThread(Thread):

    def __init__(self, client, ip, port):
        Thread.__init__(self)
        self.ip = ip 
        self.port = port
        self.set_game(client)
        
    def recv_all(self, crlf, conn):
        data = ""
        while not data.endswith(crlf):
            data += conn.recv(1).decode()
        return data[:-2]
    
    def recv_array(self, conn):
        data = conn.recv(1)
        while not data.endswith(CRLF.encode()):
            data += conn.recv(1)
        return pickle.loads(data)

    def set_game(self, client):
        client.send(codes.get_code("Available").encode() + CRLF.encode())
        try:
            response = self.recv_all(CRLF, client) #set level response
        except:
            logger.warning('Client %s disconnected', self.ip)
            return

        if response == "QuitGame" :
            self.endGame(client)
            logger.info('player %s quitting game', self.ip)
        else:
            level = int(int_from_bytes(response.encode()))
            cards_map = mapa.create_map(level) # normal array
            client.send(codes.get_code("Success").encode() + CRLF.encode())
    
            self.handle_game(client, cards_map, level)
    
    def handle_game(self, client, cards_map, level):
        self.card_sent = 0
        self.solved_pairs = 0
        while True:
            try:
                answer = self.recv_all(CRLF, client)
                if answer == "QuitGame":
                    logger.info('player quitting game' )
                    self.endGame(client)
                    break
                else:
                    client.send(cards_map[int(answer)].word.encode() + CRLF.encode()) 
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
                
            except:
                logger.warning('Client %s connection dropped', self.ip)
                break
    
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)
    
    def endGame(self, client):
        logger.info('client %s disconnected', self.ip)
        Server.remove(client)
        client.close()
        
            
if __name__ == '__main__':
    
    logger = logging.getLogger('server_logger')
    logger.setLevel(logging.INFO)
    
    fh = logging.FileHandler('server.log')
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)

    mapa = maps.Map()
    server = Server(mapa)
    server.run()
