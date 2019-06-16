# -*- coding: utf-8 -*-

import tkinter as tk
import pickle
import store.codes as codes
import store.options as options 
import store.card
import store

EOF = '\0'
CRLF = '\r\n'

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

class App:
    
    def __init__(self, root, s):
        self.s = s
        self.root = root
        self.cards_up = 0
        self.cards_to_compare = []
        self.attempts = 0
        self.pairs = 0
        self.found = False
        self.two_up = False
        self.root.title("Memorsy!")
        tk.Frame(self.root, width=500, height=450).pack()
        self.setLevel()
    
    def reset(self):
        self.cards_up = 0
        self.cards_to_compare = []
        self.attempts = 0
        self.pairs = 0
        self.two_up = False
        
    def recv_all(self, crlf):
        data = ''
        while not data.endswith(crlf):
            data = data + self.s.recv(1).decode()
        return data
    
    def get_response(self):
         response = self.recv_all(CRLF)
         print(codes.get_response_text(response))
         return int(response)
     
    def get_card_content(self, id):
        self.s.send(str(id).encode() + CRLF.encode())
        response = self.recv_all(CRLF)
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
        self.level = self.levelVal.get()
        self.s.send(int_to_bytes(self.level))
        is_map_created = self.get_response()
        if(is_map_created == int(codes.get_code('Success'))):
            self.start()
            
    def create_cards(self):
        self.cards_layout = []
        for i in range(0, options.levels[self.level]*2):
            self.cards_layout.append(store.card.Card("", False, i))

        
    def start(self):
        self.sideLen = options.levels[self.level]
        self.create_cards()
        self.print_board()

    #plansza
    def print_board(self):
        xvar=10
        yvar=70
        self.buttons = []
        cards_index = 0
        for i in range(self.sideLen):
            for j in range(options.levels[self.level]-1):

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
        print('card clicked: ', index)
        if self.cards_layout[index].up == False:

            # turn card on
            self.cards_layout[index].up = True
            self.buttons[index].config(text=self.get_card_content(index))
            self.cards_up += 1

            #clear card
            '''if self.two_up == True:
                print(' mysterious function')
                self.is_up = self.var.get()
                self.var.set("")
                self.is_up = False'''

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
                self.two_up = True
                
        else:
            text = self.var.get()
            self.var.set("Weź inna kartę")


    def compare(self):
        self.attempts += 1
        # send to server two ids
        data = pickle.dumps(self.cards_to_compare)
        self.s.send(data + CRLF.encode())
        result = self.get_response()
        if result == int(codes.get_code('PairFound')):
            self.cards_layout[self.cards_to_compare[0]].up = True
            self.cards_layout[self.cards_to_compare[1]].up = True
            text = self.var.get()
            self.found = True
            self.two_up= True
        elif result == int(codes.get_code('GameOver')):
            text = self.var.get()
            self.var.set("Gra skończona w " + str(self.attempts) + " próbach.")
            self.newGameButton = tk.Button(
                    self.root,
                    command=self.newGame,
                    text="Nowa Gra",
                    width="12")
            self.endGameButton = tk.Button(
                    self.root,
                    command=self.endGame,
                    text="Koniec",
                    width="12")
            self.newGameButton.pack()
            self.endGameButton.pack()
        else:
            self.found = False
            self.cards_layout[self.cards_to_compare[0]].up = False
            self.cards_layout[self.cards_to_compare[1]].up = False         


    def newGame(self):
        self.reset()
        self.newGameButton.pack_forget()
        self.endGameButton.pack_forget()
        code = codes.get_code('NewGame')
        self.s.send(code.encode() + CRLF.encode())
        text = self.var.get()
        self.var.set("")
        self.text = False
        self.newGameButton.destroy()
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
        self.attemps = 0
        
        self.text = False
        self.setLevel()
    
    def endGame(self):
        pass
    
def get_layout(s):
    print('*** app started')
    root = tk.Tk()
    App(root, s)
    root.mainloop()