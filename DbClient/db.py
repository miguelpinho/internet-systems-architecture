import sqlite3

from Utils.private_consts import DbAccess

def init_db(db):
    qry = open('DbClient/schema.sql', 'r').read()
    if sqlite3.complete_statement(qry):
        cursor = db.cursor()

        try:
            cursor.executescript(qry)
        except sqlite3.Error as e:
            print("Error initializing sqlite3 DB: {}".
                  format(e.args[0]))

def get_db():
    db = sqlite3.connect(DbAccess.DB_NAME)

    return db

def close_db(db):
    db.commit() # FIXME: makes sense?

    db.close()

