# -*- coding: utf-8 -*-
'''
CODES
'''
codes=[
    ("10", "Available"),
    ("11", "NotAvailable"),    
	("20", "TalkToMe"),
	("22", "Success"),    
	("34", "FileNotFound"),
    ("37", "FileFound"),
	("44", "WrongReqest"),
	("50", "ServerError"),
	("80", "Closed")
]

responses={
    10: "Memorsy! Hi There :)",
    11: "Server Not Avalible",
    20: "TalkToMe",
    22: "Success",
    37: "File found",
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
            print(i)
            return i[0]