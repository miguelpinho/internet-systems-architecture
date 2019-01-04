import requests
import random
import time
import json


def send_message():
    while True:
        possible_messages = ['Building closes at 20', 'Emergency - Leave the building', 'You know nothing John Snow']

        message = random.choice(possible_messages)

        payload = {'message': message}

        r = requests.post('/api/bot', data=payload)
        if r.status_code == 200:
            print(json.dumps(r.json()))
        else:
            print('Error:' + r.status_code + ',' + r.json()["message"])

        time.sleep(15)


