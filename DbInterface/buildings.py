import MySQLdb


def add_building(db, bid, bname, latitude, longitude, radius):
    # adds building
    cur = db.cursor()

    try:
        cur.execute("""INSERT INTO building (id, name, latitude, longitude, radius) VALUES (%s, %s, %s, %s, %s)""",
                    (bid, bname, latitude, longitude, radius))
    except MySQLdb.Error as err:
        print("Error adding building MySQLdb DB: {}".
              format(err))
    else:
        db.commit()


def delete_building(db, bid):
    # return bid info
    cur = db.cursor()

    try:
        cur.execute("""DELETE FROM building WHERE building.id = %s""",
                    (bid, ))
    except MySQLdb.Error as e:
        print("Error removing bot MySQLdb DB: {}".
              format(e.args[0]))

        return None
    else:
        db.commit()

    return bid


def show_users(db, bid):
    # return list of users in a building
    cur = db.cursor()

    try:
        cur.execute("""SELECT ist_id FROM ist_user WHERE ist_user.cur_building = %s""",
                    (bid, ))
    except MySQLdb.Error as e:
        print("Error getting all users in a building MySQLdb DB: {}".
              format(e.args[0]))

        return None

    users = cur.fetchall()

    return  [u[0] for u in users]


def show_info(db, bid):
    # return building info
    cur = db.cursor()

    try:
        cur.execute("""SELECT * FROM building WHERE building.id = %s""",
                    (bid, ))
    except MySQLdb.Error as e:
        print("Error searching bot MySQLdb DB: {}".
              format(e.args[0]))

        return []

    res = cur.fetchone()

    if res is not None:
        res = res[0:2] + tuple(float(d) for d in res[2:5])

    return res


def show_all_buildings(db):
    # return list of bids and bname
    cur = db.cursor()

    try:
        cur.execute("""SELECT * FROM building""")
    except MySQLdb.Error as e:
        print("Error searching bot MySQLdb DB: {}".
              format(e.args[0]))

        return []

    res = cur.fetchall()

    res = [(x[0:2] + tuple(float(d) for d in x[2:5])) for x in res]

    return res

