import urllib.request as ul
import json
from urllib.parse import quote
import re

from discord import message

def get_chat_data():
    url = f"http://127.0.0.1:8000/discord"

    request = ul.Request(url)
    response = ul.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        responsedata = response.read()

        my_json = responsedata.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        if data["flag"] == "success":
            print(data)
            return data["stub"]

    return "fail"

blackwordfile = open("blackword.txt", "r", encoding="UTF-8")
blackwordlist = tuple(blackwordfile.read().split("\n"))
blackwordfile.close()

filtpattFile=open("blackregex.txt", "r", encoding="UTF-8")
filtpattList = tuple(filtpattFile.read().split("\n"))
filtpattFile.close()

def CheckMessage(mess):
    global blackwordlist
    global filtpattList

    mess = mess.replace("          ", "")

    for black in filtpattList:
        mess=re.sub(black,"#",mess)

    for black in blackwordlist:
        if black in mess:
            mess = mess.replace(black, "#")
    

    

    return mess