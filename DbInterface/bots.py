import MySQLdb
from random import randint
import uuid
from Utils.consts import Datastore


def add_bot(db, bid, cache=None):
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

    if cache is not None:
        cache.set(Datastore.BOT_PREFIX + bot_token, bid)

    return bot_token


def delete_bot(db, bot_token, cache=None):
    # returns deleted bot info (got from database pop)
    cur = db.cursor()

    if cache is not None:
        cache.delete(Datastore.BOT_PREFIX + bot_token)

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


def where_is_bot(db, bot_token, cache=None):
    # return [bid] where the bot sends messages

    if cache is not None:
        bid = cache.get(Datastore.BOT_PREFIX + bot_token)
    else:
        bid = None

    if bid is None:
        # bot is not cached, get from DB

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
            return []
        else:
            bid = bid[0]

            if cache is not None:
                cache.set(Datastore.BOT_PREFIX + bot_token, bid)

    return bid


