# -*- coding: utf-8 -*-
import random
from card import Card

class Map():
    def __init__(self, level):
        self.level = level
        
    def read(self):
        file = open("cards.txt","r")
        line = file.readline()
        self.allWords = []
        while line !="":
            part = line.split("\n")
            self.allWords.append(part[0])
            line = file.readline()
        file.close()

    def random(self):
        random.shuffle(self.allWords)
        self.words = self.allWords[:int(pow(self.sideLen,2)/2)]
        
    def create_cards(self):
        self.cards = []
        for i in self.words:
            self.cards.append(Card(i,False))
            
    def create_map(self):
        self.words = self.words*2
        #random.shuffle
        #TODO: add maping (card, position in map)