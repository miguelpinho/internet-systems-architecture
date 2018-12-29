import DbClient.db as clientDB
import DbInterface.buildings as building
import DbInterface.bots as bots
import DbInterface.user as user

db = clientDB.get_db()

clientDB.init_db(db)

# TEST: add buildings
building.add_building(db, 101, "SCDEEC", 100.0, 31.1, 10.0)
building.add_building(db, 33, "civil", 310.1, 433.9, 13.0)

print(building.show_info(db, 101))
print(building.show_all_buildings(db))


# TEST: remove building
building.delete_building(db, 33)
print(building.show_all_buildings(db))


# TEST: add bots
btokens = [bots.add_bot(db, 101), bots.add_bot(db, 33), bots.add_bot(db, 101)]
print(btokens)
print(bots.list_bots(db))
print(bots.list_bots_by_building(db, 101))
print(bots.where_is_bot(db, btokens[-1]))


# TEST: delete bot
bots.delete_bot(db, btokens[-1])
btokens = btokens[0:-1]
print(btokens)
print(bots.list_bots(db))



# TEST: set user location and get current building
user.set_position(db, "ist131313", 100.0, 31.1)
print(user.get_position(db, "ist131313"))

user.clear_position(db, "ist131313")
print(user.get_position(db, "ist131313"))

user.set_position(db, "ist131313", 90.0, 41.1)
print(user.get_user_building(db, "ist131313"))


# TEST: get close users
user.set_position(db, "ist231313", 90.0, 51.1)
user.set_position(db, "ist331313", 90.0, 31.0) # This one should not appear
user.set_position(db, "ist431313", 85.0, 43.1)

print(user.get_close_users(db, "ist131313", 90.0, 41.1, 10.0))


# TEST: show all users in a building
print(building.show_users(db, 101))


