from flask import g
import DbClient


def get_db():
    if 'db' not in g:
        #  TODO: g.db = get_db_client(current_app.private_consts)
        g.db = None
    return g.db
