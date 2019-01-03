from flask import g
import DbClient


def get_db(private_consts):
    if 'db' not in g:
        #  TODO: g.db = get_db_client()
        g.db = None
    return g.db
