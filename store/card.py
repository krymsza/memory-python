# -*- coding: utf-8 -*-

class Card:

    def __init__(self,word,up):
        self.word = word
        self.up = up

    def __str__(self):
        if self.up == True:
            return self.word
        else:
            return ""
   