import requests
import argparse
import json


def parser_function():
    parser = argparse.ArgumentParser(description='Administrator App')
    parser.add_argument('-i', '--ip', type=str, metavar='', help='Used to define an ip other than the default')
    parser.add_argument('-u', '--username', type=str, metavar='', help='Used to define username to login')
    parser.add_argument('-p', '--password', type=str, metavar='', help='Used to define password to login')
    args = parser.parse_args()
    return args


def main():
    args = parser_function()

    if args.ip:
        ip = args.ip
    else:
        ip = '127.0.0.1:5000'  # default

    username = args.username
    password = args.password

    cookie = connect_to_server(ip, username, password)

    menu(ip, cookie)


def connect_to_server(ip, username, password):
    payload = {'username': username, 'password': password}
    r = requests.post('http://'+ip + '/auth/login', json=payload)
    cookie = r.cookies

    return cookie


def options_parsing(selection, ip, cookie):
    if selection == '1':
        bid = input("Enter the building ID where the new bot is to be placed:")
        add_bot(ip, cookie, bid)
    elif selection == '2':
        token = input("Enter Bot's token to be deleted:")
        delete_bot(ip, cookie, token)
    elif selection == '3':
        list_bots(ip, cookie)
    elif selection == '4':
        load_buildings(ip, cookie)
    elif selection == '5':
        token = input("Enter Bot's token to be found:")
        where_is_bot(ip, cookie, token)
    elif selection == '6':
        show_all_buildings(ip, cookie)
    elif selection == '7':
        aux = input(
            "Enter Building ID, Building Name, Latitude, Longitude and Radius, in that order, separated by spaces")
        building_args = aux.split()
        add_building(ip, cookie, building_args)
    elif selection == '8':
        bid = input("Enter the building's ID:")
        show_building(ip, cookie, bid)
    elif selection == '9':
        bid = input("Enter the building's ID, to be deleted:")
        delete_building(ip, cookie, bid)
    elif selection == '10':
        ist_id = input('Enter Users ID:')
        get_log_user(ip, cookie, ist_id)
    elif selection == '11':
        ist_id = input('Enter Users ID:')
        get_moves_user(ip, cookie, ist_id)
    elif selection == '12':
        bid = input("Enter the building's ID:")
        get_building_log(ip, cookie, bid)
    elif selection == '13':
        bid = input("Enter the building's ID:")
        show_users_in_building(ip, cookie, bid)
    elif selection == '14':
        show_logged_users(ip, cookie)
    elif selection == '0':
        pass
    else:
        print('Invalid Selection')


def menu(ip, cookie):
    menu_ = {'1': 'Add Bot', '2': 'Delete Bot', '3': 'List Bots', '4': 'Load Buildings', '5': 'Find Bot',
             '6': 'Show All Buildings', '7': 'Add Building', '8': 'Show Building', '9': 'Delete Building',
             '10': 'Show User Log', '11': 'Show User Moves', '12': 'Show Building Log','13': 'Show Users in Building',
             '14' : 'Show Logged Users', '0': 'Exit'}
    print('Welcome Admin\n')
    while True:
        options = menu_.keys()
        for entry in options:
            print(entry, menu_[entry])
        selection = input("Please select an option >> ")
        options_parsing(selection, ip, cookie)
        if selection == '0':
            break


def add_bot(ip, cookie, bid):  # POST
    payload = {'building': bid}
    r = requests.post('http://'+ip + '/api/admin/bots', json=payload, cookies=cookie)
    if r.status_code == 200:
        print('Succesfully added:' + json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def list_bots(ip, cookie):  # GET
    r = requests.get('http://'+ip + '/api/admin/bots', cookies=cookie)
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def load_buildings(ip, cookie):  # POST
    with open('buildings.json')as f:
        data = json.load(f)
    for building in data:
        add_building(ip, cookie, building)


def delete_bot(ip, cookie, token):  # DELETE
    r = requests.delete('http://'+ip + '/api/admin/bots/' + token, cookies=cookie)
    if r.status_code == 200:
        print('Succesfully deleted:' + json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def show_users_in_building(ip, cookie, bid):  # GET
    r = requests.get('http://' + ip + '/api/admin/buildings/' + bid + '/users', cookies=cookie)
    if r.status_code == 200:
        print('Succesfully loaded:' + json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def show_logged_users(ip, cookie):  # GET
    r = requests.get('http://' + ip + '/api/admin/users', cookies=cookie)
    if r.status_code == 200:
        print('Succesfully loaded:' + json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def where_is_bot(ip, cookie, token):  # GET
    r = requests.get('http://'+ip + '/api/admin/bots/' + token, cookies=cookie)
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def show_all_buildings(ip, cookie):  # GET
    r = requests.get('http://'+ip + '/api/admin/buildings', cookies=cookie)
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def add_building(ip, cookie, building_args):  # POST
    if type(building_args) is list:
        payload = {'id': building_args[0], 'name': building_args[1], 'latitude': building_args[2], 'longitude':
            building_args[3], 'radius': building_args[4]}
    else:
        payload = building_args
    r = requests.post('http://'+ip + '/api/admin/buildings', json=payload, cookies=cookie)
    if r.status_code == 200:
        print('Succesfully added:' + json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def show_building(ip, cookie, bid):  # GET
    r = requests.get('http://'+ip + '/api/admin/buildings/' + bid, cookies=cookie)
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def delete_building(ip, cookie, bid):  # DELETE
    r = requests.delete('http://'+ip + '/api/admin/buildings/' + bid, cookies=cookie)
    if r.status_code == 200:
        print('Succesfully deleted:' + json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def get_log_user(ip, cookie, ist_id):  # GET
    r = requests.get('http://'+ip + '/api/admin/logs/users/' + ist_id + '/messages', cookies=cookie)
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def get_moves_user(ip, cookie, ist_id):  # GET
    r = requests.get('http://'+ip + '/api/admin/logs/users/' + ist_id + '/moves', cookies=cookie)
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


def get_building_log(ip, cookie, bid):  # GET
    r = requests.get('http://'+ip + '/api/admin/logs/building/' + bid, cookies=cookie)
    if r.status_code == 200:
        print(json.dumps(r.json()))
    else:
        print('Error:' + str(r.status_code) + ',' + r.json()["message"])


if __name__ == "__main__":
    main()