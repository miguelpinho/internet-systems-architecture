import pymysql as MySQLdb
from Utils.consts import Datastore


def get_token(cache, token):
    # gets the user_ID associated to a token, if valid
    return cache.get(Datastore.USER_PREFIX + str(token))


def set_token(cache, token, user_id):
    # stores a token in association to a user_ID
    return cache.set(Datastore.USER_PREFIX + str(token), user_id, timeout=20*60)


def delete_token(cache, token):
    # mark a token as invalid
    cache.delete(Datastore.USER_PREFIX + str(token))


def set_position(db, ist_id, latitude, longitude):
    # update position
    cur = db.cursor()

    try:
        cur.execute("""INSERT INTO ist_user (ist_ID, latitude, longitude) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE latitude = %s, longitude = %s""",
                    (ist_id, latitude, longitude, latitude, longitude))
    except MySQLdb.Error as err:
        print("Error set user position MySQLdb DB: {}".
              format(err))

        return None
    else:
        db.commit()

    return (latitude, longitude)


def get_position(db, ist_id):
    # return (latitude,longitude) if checked in, null otherwise
    cur = db.cursor()

    try:
        cur.execute("""SELECT latitude, longitude FROM ist_user WHERE ist_user.ist_ID = %s""",
                    (ist_id, ))
    except MySQLdb.Error as err:
        print("Error getting user location MySQLdb DB: {}".
              format(err))

        return None

    res = cur.fetchone()

    if res is not None:
        if res[0] is None or res[1] is None:
            res = None
        else:
            res = (float(res[0]), float(res[1]))

    return res


def clear_position(db, ist_id):
    # marks the postion of the user as no longer valid
    cur = db.cursor()

    try:
        cur.execute("""UPDATE ist_user SET latitude = NULL, longitude = NULL, cur_building = NULL
                    WHERE ist_user.ist_ID = %s""",
                    (ist_id, ))
    except MySQLdb.Error as err:
        print("Error clearing user location MySQLdb DB: {}".
              format(err))


def get_close_users(db, ist_id, radius):
    # return [users] of close users
    pos = get_position(db, ist_id)

    if pos is None:
        return []

    (latitude, longitude) = pos

    (lat_low, lat_high) = (latitude - radius, latitude + radius)
    (long_low, long_high) = (longitude - radius, longitude + radius)

    cur = db.cursor()

    try:
        cur.execute("""SELECT ist_id FROM ist_user WHERE latitude >= %s AND latitude <= %s
                    AND longitude >= %s AND longitude <= %s AND ist_id <> %s""",
                    (lat_low, lat_high, long_low, long_high, ist_id))

    except MySQLdb.Error as err:
        print("Error getting close users MySQLdb DB: {}".
              format(err))
        return []

    users = cur.fetchall()

    return  [u[0] for u in users]


def get_logged_users(db):
    # return all logged users
    cur = db.cursor()

    try:
        cur.execute("""SELECT ist_id FROM ist_user WHERE latitude IS NOT NULL AND longitude IS NOT NULL""")

    except MySQLdb.Error as err:
        print("Error getting logged users MySQLdb DB: {}".
              format(err))
        return []

    users = cur.fetchall()

    return  [u[0] for u in users]


def get_user_building(db, ist_id):
    # return building where user is if checked in, null otherwise
    cur = db.cursor()

    try:
        cur.execute("""SELECT cur_building FROM ist_user WHERE ist_user.ist_ID = %s""",
                    (ist_id, ))
    except MySQLdb.Error as err:
        print("Error getting user building MySQLdb DB: {}".
              format(err))

        return None

    res = cur.fetchone()

    if res is not None:
        res = res[0]

    return res
