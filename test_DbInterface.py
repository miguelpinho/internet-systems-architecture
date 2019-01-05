import DbClient.db as clientDB
import DbInterface.buildings as building
import DbInterface.bots as bots
import DbInterface.user as user
import DbInterface.logs as log
from Utils.consts import configure_private_consts

db = clientDB.get_db(configure_private_consts())

clientDB.init_db(db)

# TEST: add buildings
building.add_building(db, 101, "asdas", 100.0, 31.1, 10.0)
building.add_building(db, 33, "civil2", 310.1, 433.9, 13.0)

print(building.show_info(db, 101))
print(building.show_all_buildings(db))


# TEST: remove building
# building.delete_building(db, 33)
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
user.set_position(db, "ist131313", 310.0, 433.1)
print(user.get_position(db, "ist131313"))

user.clear_position(db, "ist131313")
print(user.get_position(db, "ist131313"))
print(user.get_user_building(db, "ist131313"))

user.set_position(db, "ist131313", 90.0, 41.1)
print(user.get_user_building(db, "ist131313"))


# TEST: get close users
user.set_position(db, "ist231313", 90.0, 51.1)
user.set_position(db, "ist331313", 90.0, 31.0) # This one should not appear
user.set_position(db, "ist431313", 85.0, 43.1)
print(user.get_close_users(db, "ist131313", 10.0))

user.clear_position(db, "ist431313")
print(user.get_close_users(db, "ist131313", 10.0))

user.set_position(db, "ist331313", 310, 433)
user.clear_position(db, "ist331313")
user.set_position(db, "ist331313", 10, 10)

# TEST: show all users in a building
print(building.show_users(db, 101))


# TEST: user message log
log.store_msg_user(db, "ist431313", "messagem A1")
log.store_msg_user(db, "ist131313", "messagem B1")
log.store_msg_user(db, "ist131313", "messagem B2")
log.store_msg_user(db, "ist431313", "messagem A2")
log.store_msg_user(db, "ist431313", "messagem A3")
log.store_msg_user(db, "ist431313", "messagem A4")
log.store_msg_user(db, "ist431313", "messagem A5")
log.store_msg_user(db, "ist131313", "messagem B3")
log.store_msg_user(db, "ist131313", "messagem B4")

print(log.get_msgs_user(db, "ist431313"))
print(log.get_msgs_user(db, "ist131313"))


# TEST: building message log
log.store_msg_building(db, 101, "messagem C1")
log.store_msg_building(db, 33, "messagem D1")

log.store_msg_building(db, 101, "messagem C2")
log.store_msg_building(db, 33, "messagem D2")
log.store_msg_building(db, 101, "messagem C3")
log.store_msg_building(db, 33, "messagem D3")

print(log.get_msgs_building(db, 101))
print(log.get_msgs_building(db, 33))


# TEST: moves user log
print(log.get_moves(db, "ist331313"));


