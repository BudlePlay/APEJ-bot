import urllib.request as ul
import json
from urllib.parse import quote


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


def CheckMessage(message):
    blackwordfile = open("blackword.txt", "r", encoding="UTF-8")

    blackwordlist = blackwordfile.read().split("\n")
    blackwordfile.close()

    for black in blackwordlist:
        if black in message:
            message = message.replace(black, "##")

    return message
