import os

import MySQLdb

def init_db(db):
    cursor = db.cursor()

    for line in open('DbClient/reset.sql'):
        try:
            cursor.execute(line)
        except MySQLdb.Error as err:
            print("Error initializing mysql DB: {}".
                  format(err.args[0]))

            return


def get_db(private_consts):
    db_const = private_consts.DatabaseKeys

    try:
        if os.environ.get("GAE_ENV") == "standard":
            db = MySQLdb.connect(
                    unix_socket='/cloudsql/{}'.format(
                        db_const.MYSQL_DATABASE_CONNECTION_NAME),
                    user=db_const.MYSQL_DATABASE_USER,
                    db=db_const.MYSQL_DATABASE_NAME,
                    password=db_const.MYSQL_DATABASE_PW,

                )
        else:
            db = MySQLdb.connect(user=db_const.MYSQL_DATABASE_USER,
                                 password=db_const.MYSQL_DATABASE_PW,
                                 host=db_const.MYSQL_DATABASE_HOST,
                                 database=db_const.MYSQL_DATABASE_NAME)

    except MySQLdb.Error as err:
        print("Error connecting to DB: {}".
              format(str(err)))
        return None

    return db


def close_db(db):
    db.close()
