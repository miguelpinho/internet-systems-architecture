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

PRIVATE_CONSTS_JSON_FILE_PATH = "private_consts.json"


class AuthType:
    AUTH_TYPE_ADMIN = "Admin"
    AUTH_TYPE_USER = "User"
    AUTH_TYPE_BOT = "Bot"


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


class PrivateConsts:
    class FenixApiKeys:
        FENIX_API_CLIENT_ID = "Put your own fenix api id"  # This is a default values
        FENIX_API_CLIENT_SECRET = "Put your own fenix api Secret"

    # Here you can add another classes like FenixApiKeys
    # class MySpecialKeys:
    #   BLABLA_SUPER_SECRET = "SECRET"
    class DatabaseKeys:
        POSTGRE_DATABASE_NAME = "Put the postgre database name"
        POSTGRE_DATABASE_USER = "Put the postgre database user"
        POSTGRE_DATABASE_HOST = "Put the postgre host ip here"
        POSTGRE_DATABASE_PW = "Put the postgre password"


if __name__ == "__main__":
    configure_private_consts()
    print(PrivateConsts.FenixApiKeys.FENIX_API_CLIENT_ID)
    print(PrivateConsts.FenixApiKeys.FENIX_API_CLIENT_SECRET)
