# -*- coding: utf-8 -*-
import random
from store.card import Card


class Map(object):
    levels= { 1: 3, 2: 5}
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
        random.shuffle(self.allWords)               # mix all cards
        self.words = self.allWords[:int(self.levels[level])]
        
    def create_cards(self):
        self.cards = []
        i = 0
        for word in self.words:
            self.cards.append(Card(word, False, i))
            i+=1

    #TODO: add maping (card, position in map)       
    def create_map(self, level):
        self.random(level)                          # drawing cards from file
        self.words = self.words*2
        print('words draw for deck: ', self.words)
        self.create_cards()
        random.shuffle(self.cards)
        return  self.cards
        