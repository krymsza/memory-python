# -*- coding: utf-8 -*-
import random
from store.card import Card
import store.options as options 


class Map(object):
    def __init__(self,):
        self.read()
        pass
        
    def read(self):
        file = open("../store/cards.txt","r")
        line = file.readline()
        self.allWords = []
        while line !="":
            part = line.split("\n")
            self.allWords.append(part[0])
            line = file.readline()
        file.close()

    def random(self, level):
        random.shuffle(self.allWords)        # mix all cards
        self.words = self.allWords[:int(options.levels[level])]
        
    def create_cards(self):
        self.cards = []
        i = 0
        for word in self.words:
            self.cards.append(Card(word, False, i))
            i+=1
     
    def create_map(self, level):
        self.random(level)                   # drawing cards from file
        self.words = self.words*2
        self.create_cards()
        random.shuffle(self.cards)
        return  self.cards
        