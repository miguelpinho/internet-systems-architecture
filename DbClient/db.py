import psycopg2

# from Utils.private_consts import DbAccess

def init_db(db):
    qry = open('DbClient/schema.sql', 'r').read()

    cursor = db.cursor()

    try:
        cursor.execute(qry)
    except psycopg2.Error as e:
        print("Error initializing sqlite3 DB: {}".
              format(e.args[0]))
    finally:
        cursor.close()


def get_db():
    try:
        # db = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format())
        db = psycopg2.connect(user = , password = , host = , database = )
    except:
        print("Error connecting to DB")
        return None

    return db

def close_db(db):
    db.close()

