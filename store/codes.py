# -*- coding: utf-8 -*-
'''
CODES
'''
codes=[
    ("10", "Available"),
    ("11", "NotAvailable"),
    ("14", "NewGame"),
    ("17", "EndGame"),
    ("19", "QuitGame"),
	("20", "Success"),
	("22", "PairFound"),    
	("24", "PairNotFound"),
    ("27", "GameOver"),
	("44", "FileNotFound"),
	("50", "ServerError"),
	("80", "Closed")
]

responses={
    10: "Memorsy! Hi There :)",
    11: "Server Not Avalible",
    14: "Nowa gra",
    17: "Koniec",
    19: "Wychodzenie z gry",
    20: "Success",
    22: "It's a pair!",
    24: "Try again",
    27: "Game Over",
    44: "Could not connect to database",
	50: "Server error",
	80: "Goodbye :)"
}

def get_response_text(code):
    if type(code) != int:
        code=int(code)
    return responses[code]

def get_code(text):
    for i in codes:
        if i[1] == text:
            #print(i)
            return i[0]