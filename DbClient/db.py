import sqlite3

from Utils.private_consts import DbAccess

def init_db(db):
    db.

def get_db():
    db = sqlite3.connect(DbAccess.DB_NAME)

    return db

def close_db(db):
    db.

