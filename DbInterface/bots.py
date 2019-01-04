import MySQLdb
from random import randint
import uuid

def add_bot(db, bid):
    # adds bot (creates bot token and puts time of creation in
    # the record and return the token in the end
    bot_token = uuid.uuid4().hex

    cur = db.cursor()

    try:
        cur.execute("""INSERT INTO bot (token, building) VALUES (%s, %s)""",
                    (bot_token, bid))
    except MySQLdb.Error as err:
        print("Error adding bot MySQLdb DB: {}".
              format(err))
    else:
        db.commit()

    # TODO: Put in cache?

    return bot_token


def delete_bot(db, bot_token):
    # returns deleted bot info (got from database pop)
    cur = db.cursor()

    #TODO: Remove from cache?

    try:
        cur.execute("""DELETE FROM bot WHERE bot.token = %s""",
                    (bot_token, ))
    except MySQLdb.Error as err:
        print("Error removing bot MySQLdb DB: {}".
              format(err))
    else:
        db.commit()


def list_bots_by_building(db, bid):
    # return list of bots in a building (if there are no bots a empty list is returned)
    cur = db.cursor()

    try:
        cur.execute("""SELECT bot.token FROM bot WHERE bot.building = %s""",
                    (bid, ))
    except MySQLdb.Error as err:
        print("Error searching bots by building MySQLdb DB: {}".
              format(err))

        return []

    bots = cur.fetchall()
    return [b[0] for b in bots]


def list_bots(db):
    # return list of existing bots
    cur = db.cursor()

    try:
        cur.execute("""SELECT bot.token FROM bot""")
    except MySQLdb.Error as err:
        print("Error searching bots by building MySQLdb DB: {}".
              format(err))

        return []

    bots = cur.fetchall()
    return [b[0] for b in bots]


def where_is_bot(db, bot_token):
    # return [bid or bname] where the bot sends messages

    # TODO: try to get from cache

    # FIXME: this is for bid, but it is easy to change
    cur = db.cursor()

    try:
        cur.execute("""SELECT bot.building FROM bot WHERE bot.token = %s""",
                    (bot_token, ))
    except MySQLdb.Error as err:
        print("Error searching bot MySQLdb DB: {}".
              format(err))

        return []

    bid = cur.fetchone()

    if bid is None:
        pass # TODO: no bot with that token
    else:
        bid = bid[0]

    # TODO: add to cache if found

    return bid


