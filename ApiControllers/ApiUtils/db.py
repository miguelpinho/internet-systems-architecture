from flask import g, current_app
from DbClient.db import get_db as get_db_client


def get_db():
    if 'db' not in g:
        g.db = get_db_client(current_app.private_consts)

    return g.db
