import psycopg2

def set_position(db, ist_id, latitude, longitude):
    # update position
    cur = db.cursor()

    try:
        cur.execute("INSERT or REPLACE INTO ist_user (ist_ID, latitude, longitude) VALUES (%(ist_id)s, %(lat)s, %(long)s);",
                    {"ist_id": ist_id, "lat": latitude, "long": longitude})
    except psycopg2.Error as e:
        print("Error set user position psycopg2 DB: {}".
              format(e.args[0]))

        return None
    else:
        db.commit()
    finally:
        cur.close()

    return (latitude, longitude)


def get_position(db, ist_id):
    # return (latitude,longitude) if checked in, null otherwise
    cur = db.cursor()

    try:
        cur.execute("SELECT latitude, longitude FROM ist_user WHERE ist_user.ist_ID = %(ist_id)s;",
                    {"ist_id": ist_id})
    except psycopg2.Error as e:
        print("Error getting user location psycopg2 DB: {}".
              format(e.args[0]))

        return None
    finally:
        cur.close()

    res = cur.fetchone()

    if res[0] is None or res[1] is None:
        res = None

    return res


def clear_position(db, ist_id):
    # marks the postion of the user as no longer valid
    cur = db.cursor()

    try:
        cur.execute("UPDATE ist_user SET latitude = null, longitude = null, cur_building = null WHERE ist_user.ist_ID = %(ist_id)s;",
                    {"ist_id": ist_id})
    except psycopg2.Error as e:
        print("Error clearing user location psycopg2 DB: {}".
              format(e.args[0]))
    finally:
        cur.close()


def get_close_users(db, ist_id, radius):
    # return [users] of close users
    pos = get_position(db, ist_id)

    if pos in None:
        return None

    (latitude, longitude) = pos

    (lat_low, lat_high)  = (latitude - radius, latitude + radius)
    (long_low, long_high)  = (longitude - radius, longitude + radius)

    cur = db.cursor()

    try:
        cur.execute("SELECT ist_id FROM ist_user WHERE latitude >= %(lat_low)s AND latitude <= %(lat_high)s \
                    AND longitude >= %(long_low)s AND longitude <= %(long_high)s AND ist_id <> %(ist_id)s;",
                    {"ist_id": ist_id, "lat_low": lat_low, "lat_high":lat_high,
                    "long_low":long_low, "long_high": long_high})

    except psycopg2.Error as e:
        print("Error getting close users psycopg2 DB: {}".
              format(e.args[0]))
    finally:
        cur.close()

    users = cur.fetchall()

    return  [u[0] for u in users]


def get_user_building(db, ist_id):
    # return building where user is if checked in, null otherwise
    cur = db.cursor()

    try:
        cur.execute("SELECT cur_building FROM ist_user WHERE ist_user.ist_ID = %(ist_id)s;",
                    {"ist_id": ist_id})
    except psycopg2.Error as e:
        print("Error getting user building psycopg2 DB: {}".
              format(e.args[0]))

        return None
    finally:
        cur.close()

    res = cur.fetchone()

    if res is not None:
        res = res[0]

    return res


def get_userid_from_cookie(cookie):
    # get from cache -> get(cookie)
    # return None if nothing found
    pass
