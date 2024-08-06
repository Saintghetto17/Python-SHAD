import json
import requests
import time
import sys

BOT_SECRET = # your secret goes here
CHAT_ID = # your chat id hoes here
LINK = "https://api.telegram.org/bot" + BOT_SECRET + "/sendMessage"

MAX_SENDING_ATTEMPTS = 10

def send(message="Я сделаль"):
    message_data = {"chat_id": CHAT_ID, "text": message}

    is_sended = False
    attempts = 0
    while not is_sended and attempts < MAX_SENDING_ATTEMPTS:
        try:
            r1 = requests.get(LINK, params=message_data)
            is_sended = json.loads(r1.text)["ok"]
        except Exception:
            pass
        if not is_sended:
            time.sleep(2**attempts)
            attempts += 1
    if not is_sended:
        sys.stderr.write("Can't send:\n" + message)
