import sqlite3

def add_bot(db, bid):
    # adds bot (creates bot token and puts time of creation in
    # the record and return the token in the end
    bot_token = 0 # TODO

    cur = db.cursor()

    try:
        cur.execute("INSERT INTO bot VALUES (:bot_token, :bot_build);",
            {"bot_token": bot_token, "bid": bid})
    except sqlite3.Error as e:
        print("Error adding bot sqlite3 DB: {}".
              format(e.args[0]))
    else:
        db.commit()

    # TODO: Put in cache?


def delete_bot(db, bot_token):
    # returns deleted bot info (got from database pop)
    cur = db.cursor()

    #TODO: Remove from cache?

    try:
        cur.execute("DELETE FROM bot WHERE bot.token = :bot_token;",
                    {"bot_token": bot_token})
    except sqlite3.Error as e:
        print("Error removing bot sqlite3 DB: {}".
              format(e.args[0]))
    else:
        db.commit()


def list_bots_by_building(db, bid):
    # return list of bots in a building (if there are no bots a empty list is returned)
    cur = db.cursor()

    try:
        cur.execute("SELECT bot.token FROM bot WHERE bot.building = :bid;",
                    {"bid": bid})
    except sqlite3.Error as e:
        print("Error searching bots by building sqlite3 DB: {}".
              format(e.args[0]))

        return []

    return cur.fetchall()


def list_bots(db):
    # return list of existing bots
    cur = db.cursor()

    try:
        cur.execute("SELECT bot.token FROM bot;")
    except sqlite3.Error as e:
        print("Error searching bots by building sqlite3 DB: {}".
              format(e.args[0]))

        return []

    return cur.fetchall()


def where_is_bot(db, bot_token):
    # return [bid or bname] where the bot sends messages

    # TODO: try to get from cache

    # FIXME: this is for bid, but it is easy to change
    cur = db.cursor()

    try:
        cur.execute("SELECT bot.building FROM bot WHERE bot.token = :bot_token;",
                    {"bot_token": bot_token})
    except sqlite3.Error as e:
        print("Error searching bot sqlite3 DB: {}".
              format(e.args[0]))

        return []

    bid = cur.fetchone()

    if bid is None:
        pass # TODO: no bot with that token
    else:
        bid = bid[0]

    # TODO: add to cache if found

    return bid


def send_msg(db, bot_token, message):
    # return message of bot

    # FIXME: what should I do?
    pass
