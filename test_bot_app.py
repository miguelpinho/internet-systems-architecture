import requests
import random
import time
import json
import argparse


def send_message(ip, token):
    while True:
        possible_messages = ['Building closes at 20', 'Emergency - Leave the building', 'You know nothing John Snow']

        message = random.choice(possible_messages)

        payload = {'message': message, 'token': token}

        r = requests.post(ip+'/api/bot', json=payload)
        if r.status_code == 200:
            print(json.dumps(r.json()))
        else:
            print('Error:' + r.status_code + ',' + r.json()["message"])

        time.sleep(15)


def main():
    parser = argparse.ArgumentParser(description='Bot App used to test bot sending a message to the API')
    parser.add_argument('-i', '--ip', type=str, metavar='', help='Used to define an ip other than the default')
    parser.add_argument('-t', '--token', type=str, metavar='', help='Token that identifies a bot')
    args = parser.parse_args()

    if args.ip:
        ip = args.ip
    else:
        ip = 'http://127.0.0.1:5000'  # default

    send_message(ip, args.token)


if __name__ == "__main__":
    main()