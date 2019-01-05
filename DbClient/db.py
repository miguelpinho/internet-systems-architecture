import MySQLdb

def init_db(db):
    cursor = db.cursor()

    for line in open('DbClient/reset.sql'):
        cursor.execute(line)

    try:
        cursor.execute(qry)
    except MySQLdb.Error as err:
        print("Error initializing mysql DB: {}".
              format(err.args[0]))


def get_db(private_consts):
    db_const = private_consts.DatabaseKeys

    try:
        db = MySQLdb.connect(user=db_const.MYSQL_DATABASE_USER,
                             password=db_const.MYSQL_DATABASE_PW,
                             host=db_const.MYSQL_DATABASE_HOST,
                             database=db_const.MYSQL_DATABASE_NAME)
    except MySQLdb.Error as err:
        print("Error connecting to DB: {}".
              format(err.args[0]))
        return None

    return db


def close_db(db):
    db.close()
