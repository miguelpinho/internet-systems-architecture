import MySQLdb

def store_msg_user(db, ist_id, msg):
    cur = db.cursor()

    try:
        cur.execute("""INSERT INTO message_user (ist_id, message)
                    VALUES (%s, %s)""", (ist_id, msg))
    except MySQLdb.Error as err:
        print("Error adding user msg log MySQLdb DB: {}".
              format(err))
    else:
        db.commit()


def store_msg_building(db, bid, msg):
    cur = db.cursor()

    try:
        cur.execute("""INSERT INTO message_building (building, message)
                    VALUES (%s, %s)""", (bid, msg))
    except MySQLdb.Error as err:
        print("Error adding building msg log MySQLdb DB: {}".
              format(err))
    else:
        db.commit()


def get_moves(db, ist_id):
    # returns user moves by insertion order

    cur = db.cursor()

    try:
        cur.execute("""SELECT building, state FROM moves_user
                    WHERE ist_ID = %s ORDER BY id""", (ist_id, ))

    except MySQLdb.Error as err:
        print("Error getting user move log MySQLdb DB: {}".
              format(err))

    moves = cur.fetchall()

    return list(moves)


def get_msgs_user(db, ist_id):
    # returns user msg log by insertion order

    cur = db.cursor()

    try:
        cur.execute("""SELECT message FROM message_user
                    WHERE ist_ID = %s ORDER BY id""", (ist_id, ))

    except MySQLdb.Error as err:
        print("Error getting user msg log MySQLdb DB: {}".
              format(err))

    msgs = cur.fetchall()

    return [m[0] for m in msgs]


def get_msgs_building(db, bid):
    # returns building msg log by insertion order

    cur = db.cursor()

    try:
        cur.execute("""SELECT message FROM message_building
                    WHERE building = %s ORDER BY id""", (bid, ))

    except MySQLdb.Error as err:
        print("Error getting user msg log MySQLdb DB: {}".
              format(err))

    msgs = cur.fetchall()

    return [m[0] for m in msgs]

