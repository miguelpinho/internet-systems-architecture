import sqlite3

def add_building(db, bid, bname, latitude, longitude, radius):
    # adds building
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO building (id, name, latitude, longitude, radius) \
                    VALUES (:bid, :bname, :lat, :long, :radius);",
                    {"bid": bid, "bname": bname, "lat": latitude, "long": longitude,
                    "radius":radius})
    except sqlite3.Error as e:
        print("Error adding building sqlite3 DB: {}".
              format(e.args[0]))
    else:
        db.commit()


def delete_building(db, bid):
    # return bid info
    cur = db.cursor()

    try:
        cur.execute("DELETE FROM building WHERE building.id = :bid;",
                    {"bid": bid})
    except sqlite3.Error as e:
        print("Error removing bot sqlite3 DB: {}".
              format(e.args[0]))

        return None
    else:
        db.commit()

    return bid


def show_users(db, bid):
    # return list of users in a building
    cur = db.cursor()

    try:
        cur.execute("SELECT ist_id FROM ist_user WHERE ist_user.cur_building = :bid;",
                    {"bid": bid})
    except sqlite3.Error as e:
        print("Error getting all users in a building sqlite3 DB: {}".
              format(e.args[0]))

        return None

    users = cur.fetchall()

    return  [u[0] for u in users]


def show_info(db, bid):
    # return building info
    cur = db.cursor()

    try:
        cur.execute("SELECT * FROM building WHERE building.id = :bid;",
                    {"bid": bid})
    except sqlite3.Error as e:
        print("Error searching bot sqlite3 DB: {}".
              format(e.args[0]))

        return []

    return cur.fetchone()


def show_all_buildings(db):
    # return list of bids and bname
    cur = db.cursor()

    try:
        cur.execute("SELECT * FROM building;")
    except sqlite3.Error as e:
        print("Error searching bot sqlite3 DB: {}".
              format(e.args[0]))

        return []

    return cur.fetchall()

