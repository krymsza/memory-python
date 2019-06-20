# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import pickle
import logging
import store.codes as codes
import store.options as options 
import store.card

EOF = '\0'
CRLF = '\r\n'
logger = logging.getLogger('client_logger')

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

class App:
    
    def __init__(self, root, client, s):
        self.s = s
        self.client = client
        self.root = root
        self.cards_up = 0
        self.cards_to_compare = []
        self.attempts = 0
        self.pairs = 0
        self.found = False
        self.root.title("Memorsy!")
        tk.Frame(self.root, width=500, height=400).pack()
        self.setLevel()
    
    def reset(self):
        self.cards_up = 0
        self.cards_to_compare = []
        self.attempts = 0
        self.pairs = 0
     
    def get_card_content(self, id):
        self.s.send(str(id).encode() + CRLF.encode())
        response = self.client.recv_all(CRLF)
        return response

    def setLevel(self):
        self.var = tk.StringVar()
        self.txt = tk.Label(self.root, textvariable=self.var).place(x=0, y=0)
        self.var.set("")
                                      
        self.levelVal = tk.IntVar()
        self.radiobuttons = []
        for i in range(2):
            self.radiobuttons.append(tk.Radiobutton (
                    self.root,
                    text="level "+str(i+1),
                    variable=self.levelVal,
                    value=(i+1),
                    command=self.send
                    ))
            self.radiobuttons[i].pack(anchor = tk.W)

    def send(self):
        self.radiobuttons[0].pack_forget()
        self.radiobuttons[1].pack_forget()
        
        self.level = self.levelVal.get()
        # sending int 
        self.s.send(int_to_bytes(self.level) + CRLF.encode())
        is_map_created = self.client.get_response()
        if(is_map_created == int(codes.get_code('Success'))):
            self.start()
            
    def create_cards(self):
        self.cards_layout = []
        for i in range(0, options.levels[self.level]*2):
            self.cards_layout.append(store.card.Card("", False, i))
        
    def start(self):
        self.sideLen = 2  #options.levels[self.level]
        self.create_cards()
        self.print_board()


    def print_board(self):
        xvar=10
        yvar=70
        self.buttons = []
        cards_index = 0
        for i in range(self.sideLen):
            for j in range(options.levels[self.level]):

                cmd = lambda index = cards_index: self.click(index)
                self.buttons.append(tk.Button(
                        self.root,
                        command=cmd,
                        text=self.cards_layout[cards_index].word,
                        width="6"
                        ))
                self.buttons[cards_index].place(x=xvar, y=yvar)
                
                xvar=xvar+80
                cards_index += 1
            xvar=10
            yvar=yvar+60

        text = self.var.get()
        self.var.set("")
        
        for i in range(len(self.radiobuttons)):
            self.radiobuttons[i].pack_forget()

    def click(self,index):
        if self.cards_layout[index].up == False:

            # turn card on
            self.cards_layout[index].up = True
            self.buttons[index].config(text=self.get_card_content(index))
            self.cards_up += 1

            #clears button if 2 click
            if len(self.cards_to_compare) == 2:
                if self.found ==  True:
                    self.buttons[self.cards_to_compare[0]].pack_forget()
                    self.buttons[self.cards_to_compare[1]].pack_forget()
                else:
                    self.buttons[self.cards_to_compare[0]].config(
                            text= self.cards_layout[self.cards_to_compare[0]]
                            )
                    self.buttons[self.cards_to_compare[1]].config(
                            text= self.cards_layout[self.cards_to_compare[1]]
                            )
                self.cards_to_compare = []
    
            #add cards to compare & compare if 2
            if self.cards_up == 2:
                self.cards_up = 0
                self.cards_to_compare.append(index)
                self.compare()
            else:
                self.cards_to_compare.append(index)
                
        else:
            text = self.var.get()
            self.var.set("Choose another card")

    def compare(self):
        self.attempts += 1
        # send to server two ids
        logger.info('card %d , %d comparing',self.cards_to_compare[0], self.cards_to_compare[1])
        data = pickle.dumps(self.cards_to_compare)
        self.s.send(data + CRLF.encode())
        result = self.client.get_response()
        if result == int(codes.get_code('PairFound')):
            logger.info('these cards are match')
            self.cards_layout[self.cards_to_compare[0]].up = True
            self.cards_layout[self.cards_to_compare[1]].up = True
            text = self.var.get()
            self.found = True
        elif result == int(codes.get_code('GameOver')):
            logger.info('Game is over')
            text = self.var.get()
            self.var.set("Game won in " + str(self.attempts) + " attempts.")
            self.newGameButton = tk.Button(
                    self.root,
                    command=self.newGame,
                    text="New Game",
                    width="12")
            self.endGameButton = tk.Button(
                    self.root,
                    command=self.endGame,
                    text="End",
                    width="12")
            self.newGameButton.pack()
            self.endGameButton.pack()
        else:
            logger.info('these cards are different')
            self.found = False
            self.cards_layout[self.cards_to_compare[0]].up = False
            self.cards_layout[self.cards_to_compare[1]].up = False         


    def newGame(self):
        logger.info('starting new game')
        self.reset()
        self.newGameButton.pack_forget()
        self.endGameButton.pack_forget()
        code = codes.get_code('NewGame')
        self.s.send(code.encode() + CRLF.encode())
        result = self.client.get_response()
        if result == int(codes.get_code("Available")):
            text = self.var.get()
            self.var.set("")
            self.text = False
            self.newGameButton.destroy()
            for i in range(len(self.buttons)):
                self.buttons[i].destroy()
            for i in range(len(self.radiobuttons)):
                self.radiobuttons[i].destroy()
            self.attemps = 0
            
            self.text = False
            self.setLevel()
        else:
            logger.error('%s', codes.get_response_text(50))
            self.s.close()
    
    def endGame(self):
        logger.info('quitting game')
        code = codes.get_code('EndGame')
        self.s.send(code.encode() + CRLF.encode())
        self.quit()
        
    def quit(self):
        self.root.destroy()
        self.s.close()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            #TODO: change this to some high code
            self.s.send(('QuitGame').encode() + CRLF.encode())
            self.s.close()  

def get_layout(cli, s):
    logger.info('*** app started')   
    root = tk.Tk()
    app = App(root, cli, s)
    root.protocol("WM_DELETE_WINDOW",app.on_closing)
    root.mainloop()