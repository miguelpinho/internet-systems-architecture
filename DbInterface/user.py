import sqlite3

def check_in(db, ist_id):
    pass


def check_out(db, ist_id):
    pass


def send_msg(db, ist_id, msg):
    pass


def get_msgs(db, ist_id):
    # return [msg] list
    pass


def set_position(db, ist_id, latitude, longitude):
    # update position
    cur = db.cursor()

    try:
        cur.execute("UPDATE ist_user SET ist_user.latitude = :lat,\
                    ist_user.longitude = :long WHERE ist_user.ist_id = :ist_id;",
                    {"ist_id": ist_id, "lat": latitude, "long": longitude})
    except sqlite3.Error as e:
        print("Error set user position sqlite3 DB: {}".
              format(e.args[0]))

        return None
    else:
        db.commit()

    return (latitude, longitude)


def set_radius(db, ist_id, radius):
    cur = db.cursor()

    try:
        cur.execute("UPDATE ist_user SET ist_user.radius = :radius,\
                    WHERE ist_user.ist_id = :ist_id;",
                    {"ist_id": ist_id, "radius": radius})
    except sqlite3.Error as e:
        print("Error set user radius sqlite3 DB: {}".
              format(e.args[0]))

        return None
    else:
        db.commit()

    return radius


def get_position(db, ist_id):
    # return (latitude,longitude) if checked in, null otherwise
    cur = db.cursor()

    try:
        cur.execute("SELECT latitude, longitude FROM ist_user WHERE ist_user.ist_ID = :ist_id;",
                    {"ist_id": ist_id})
    except sqlite3.Error as e:
        print("Error getting user location sqlite3 DB: {}".
              format(e.args[0]))

        return None

    res = cur.fetchone()

    if res is not None:
        res = tuple(res)

    return res


def get_close_users(db, ist_id):
    # return [users] list if checked in, null otherwise
    pass

def get_user_building(db, ist_id):
    # return building where user is if checked in, null otherwise
    pass
