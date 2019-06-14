# -*- coding: utf-8 -*-

import socket
import thread
import codes

class SocketServer(socket.socket):
    clients = []

    def __init__(self):
        try:
            socket.socket.__init__(self)
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.bind(('127.0.0.1', 8080))
            self.listen(5)
        except:
            print(codes.get_response_text(11))

    def run(self):
        try:
            self.accept_clients()
        except Exception as ex:
            print ex
        finally:
            for client in self.clients:
                client.close()
            self.close()

    def accept_clients(self):
        while 1:
            (clientsocket, address) = self.accept()
            self.clients.append(clientsocket)
            self.onopen(clientsocket)
            thread.start_new_thread(self.recieve, (clientsocket,))

    def recieve(self, client):
        while 1:
            data = client.recv(1024)
            if data == '':
                break
            #Message Received
            self.onmessage(client, data)
        #Removing client from clients list
        self.clients.remove(client)
        #Client Disconnected
        self.onclose(client)
        #Closing connection with client
        client.close()
        #Closing thread
        thread.exit()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def on_open(self, client):
        try:
            self.conn.send(codes.get_code("Available").encode() + CRLF.encode())
            
        except Exception:
             print(codes.get_code("ServerError").encode() + CRLF.encode())
        pass

    def on_message(self, client, message):
        pass

    def on_close(self, client):
        pass