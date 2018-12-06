import sqlite3

from Utils.private_consts import DbAccess

def init_db(db):
    qry = open('DbClient/schema.sql', 'r').read()
    sqlite3.complete_statement(qry)
    cursor = db.cursor()

    try:
        cursor.executescript(qry)

def get_db():
    db = sqlite3.connect(DbAccess.DB_NAME)

    return db

def close_db(db):
    db.close()

