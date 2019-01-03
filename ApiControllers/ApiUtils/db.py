from flask import g
from DbClient.db import get_db as get_db_client


def get_db():
    if 'db' not in g:
        #  TODO: g.db = get_db_client()
        g.db = None
    return g.db
