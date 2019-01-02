import sqlite3

# def store_move(db, ist_id, latitude, longitude):
#     pass


def store_msg_user(db, ist_id, msg):
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO message_user (ist_id, message) \
                    VALUES (:ist_id, :msg);", {"ist_id": ist_id, "msg": msg})
    except sqlite3.Error as e:
        print("Error adding user msg log sqlite3 DB: {}".
              format(e.args[0]))
    else:
        db.commit()


def store_msg_building(db, bid, msg):
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO message_building (building, message) \
                    VALUES (:bid, :msg);", {"bid": bid, "msg": msg})
    except sqlite3.Error as e:
        print("Error adding building msg log sqlite3 DB: {}".
              format(e.args[0]))
    else:
        db.commit()


# def get_moves(db, ist_id):
#     pass


def get_msgs_user(db, ist_id):
    # returns user msg log by inverse insertion order

    # TODO: arg with number o msgs to get? None or non-positve gets all

    cur = db.cursor()

    try:
        cur.execute("SELECT message FROM message_user WHERE ist_ID = :ist_id \
                    ORDER BY id DESC;", {"ist_id": ist_id})

    except sqlite3.Error as e:
        print("Error getting user msg log sqlite3 DB: {}".
              format(e.args[0]))

    msgs = cur.fetchall()

    return [m[0] for m in msgs]


def get_msgs_building(db, bid):
    # returns building msg log by inverse insertion order

    # TODO: arg with number o msgs to get? None or non-positve gets all

    cur = db.cursor()

    try:
        cur.execute("SELECT message FROM message_building WHERE building = :bid \
                    ORDER BY id DESC;", {"bid": bid})

    except sqlite3.Error as e:
        print("Error getting user msg log sqlite3 DB: {}".
              format(e.args[0]))

    msgs = cur.fetchall()

    return [m[0] for m in msgs]

