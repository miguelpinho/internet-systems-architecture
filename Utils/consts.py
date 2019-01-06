""" This consts file has two consts publics and privates

    The privates are imported (in this order) from:
        - environment variables
        - private_consts.json  -> this file needs to be in the Utils directory
        - default values -> see below

    The publics are the ones not in the PrivateConsts class, can only be changed manually and the values are available
    on github


    Lastly, don't be afraid of asking about what I was doing in the configure_private_consts function, it's really
    trippy, but I think it's worth to do in python
"""

import json
import os

from flask import current_app

PRIVATE_CONSTS_JSON_FILE_PATH = os.path.join("Utils", "private_consts.json")
USER_DEBUG = False


class AuthType:
    AUTH_TYPE_ADMIN = "Admin"
    AUTH_TYPE_USER = "User"
    AUTH_TYPE_BOT = "Bot"


class FenixApi:
    CODE_CONFIRM_ENDPOINT = "https://fenix.tecnico.ulisboa.pt/oauth/access_token?client_id={" \
                            "client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={" \
                            "code}&grant_type=authorization_code "


class Queues:
    USER_U2U_PREFIX = "user_user_queue"
    USER_B2U_PREFIX = "bot_user_queue"
    BOTS_EXCHANGE = "bots_exchange"
    USER_EXCHANGE = "user_exchange"


class Datastore:
    USER_PREFIX = "user_"
    BOT_PREFIX = "bot_"


class Tokens:
    TOKEN_LENGHT = 20


# From here on private consts only

def configure_private_consts():
    # Open JSON private_consts file
    private_consts = {}
    try:
        private_consts_fp = open(PRIVATE_CONSTS_JSON_FILE_PATH)

        private_consts = json.load(private_consts_fp)
        private_consts_fp.close()
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print("Could not access private_consts.json file or contents are invalid:  " + str(e))

    for attrname in dir(PrivateConsts):
        if not attrname.startswith("__") and not attrname.endswith("__"):
            subclass = getattr(PrivateConsts, attrname)
            for nested_attrname in dir(subclass):
                if not nested_attrname.startswith("__") and not nested_attrname.endswith("__"):
                    # nested_attrname contains the Key name search for them in environment
                    if nested_attrname in os.environ:
                        setattr(subclass, nested_attrname, os.environ[nested_attrname])
                    # nested_attrname contains the Key name search for them in private_consts.json file
                    elif nested_attrname in private_consts:
                        setattr(subclass, nested_attrname, private_consts[nested_attrname])
    return PrivateConsts


class PrivateConsts:
    class FenixApi:
        FENIX_API_CLIENT_ID = "Put your own fenix api id"  # This is a default value
        FENIX_API_CLIENT_SECRET = "Put your own fenix api Secret"

    class Queues:
        QUEUE_HOST = "localhost"
        QUEUE_PASSWORD = "None"
        QUEUE_USER = "None"

    # Here you can add another classes like FenixApi
    # class MySpecialKeys:
    #   BLABLA_SUPER_SECRET = "SECRET"
    class DatabaseKeys:
        MYSQL_DATABASE_NAME = "Put the postgre database name"
        MYSQL_DATABASE_USER = "Put the postgre database user"
        MYSQL_DATABASE_HOST = "Put the postgre host ip here"
        MYSQL_DATABASE_PW = "Put the postgre password"

    class AdminKeys:
        ADMIN_PASSWORD = "admin"
        ADMIN_USERNAME = "admin"


if __name__ == "__main__":
    configure_private_consts()
    print(PrivateConsts.FenixApi.FENIX_API_CLIENT_ID)
    print(PrivateConsts.FenixApi.FENIX_API_CLIENT_SECRET)
