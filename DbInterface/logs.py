import psycopg2

# def store_move(db, ist_id, latitude, longitude):
#     pass


def store_msg_user(db, ist_id, msg):
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO message_user (ist_id, message) \
                    VALUES (%(ist_id)s, %(msg)s);", {"ist_id": ist_id, "msg": msg})
    except psycopg2.Error as e:
        print("Error adding user msg log psycopg2 DB: {}".
              format(e.args[0]))
    else:
        db.commit()
    finally:
        cur.close()


def store_msg_building(db, bid, msg):
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO message_building (building, message) \
                    VALUES (%(bid)s, %(msg)s);", {"bid": bid, "msg": msg})
    except psycopg2.Error as e:
        print("Error adding building msg log psycopg2 DB: {}".
              format(e.args[0]))
    else:
        db.commit()
    finally:
        cur.close()


# def get_moves(db, ist_id):
#     pass


def get_msgs_user(db, ist_id):
    # returns user msg log by inverse insertion order

    cur = db.cursor()

    try:
        cur.execute("SELECT message FROM message_user WHERE ist_ID = %(ist_id)s \
                    ORDER BY id DESC;", {"ist_id": ist_id})

    except psycopg2.Error as e:
        print("Error getting user msg log psycopg2 DB: {}".
              format(e.args[0]))
    finally:
        cur.close()

    msgs = cur.fetchall()

    return [m[0] for m in msgs]


def get_msgs_building(db, bid):
    # returns building msg log by inverse insertion order

    cur = db.cursor()

    try:
        cur.execute("SELECT message FROM message_building WHERE building = %(bid)s \
                    ORDER BY id DESC;", {"bid": bid})

    except psycopg2.Error as e:
        print("Error getting user msg log psycopg2 DB: {}".
              format(e.args[0]))
    finally:
        cur.close()

    msgs = cur.fetchall()

    return [m[0] for m in msgs]

