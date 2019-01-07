import json as json_engine
import uuid
from threading import Thread
from time import gmtime, strftime

from flask import Flask, request, current_app
from flask_socketio import SocketIO, emit, disconnect

from DbInterface.user import get_token, clear_position, set_position, get_user_building, get_position
from DbClient.db import get_db
from QueueInterface import message_queues as queue

from Utils.consts import Queues as configs, Queues


class Sockio:

    def __init__(self, private_consts, cache):
        self.cache = cache
        self.consts = private_consts
        self.channels_dict = {}

    def config_socketio(self, flask_app: Flask):
        sio = SocketIO(app=flask_app)

        @sio.on("handshake")
        def handshake_handler(json):
            """The handshake process matches the user and the socketio session
            Through this process the message queues for that user are declared and the consumption of messages is started
            """

            # json object contains the session cookie, thus identifying the sender
            # Handshake the request sid with the user identifier, through the json[data] cookie
            # get_cache(cookie) -> if there is proceed and get userid from the cache
            userid = get_token(self.cache, json["data"])
            if userid is None:
                emit('error', {'error': 'User not authenticated'})
                disconnect()
                return

            # Create message queue use this context emit to send messages
            connection = queue.connect(flask_app.private_consts.Queues.QUEUE_HOST)
            channel = queue.create_channel(connection)
            db = get_db(self.consts)
            self.channels_dict[request.sid] = {"channel": channel, "user_id": userid, "db": db, "connection": connection}

            # User2user messages
            queue_name = Queues.USER_U2U_PREFIX + "_" + str(userid) + "_" + uuid.uuid4().hex
            queue_id = queue.create_queue(channel, queue_name)
            # Bind to fanout type user exchange
            queue.bind_queue(channel, queue_id, configs.USER_EXCHANGE)

            room_id = request.sid

            def user_queue_callback(ch, method, properties, body):
                # Here filter messages by userid, only emit the ones corresponding to this user
                # if userlocation ~= messagelocation -> emit the message
                # Get user location
                data = json_engine.loads(body)
                position = get_position(db, userid)
                sender_id = data["content"]["user_id"]
                sender_position = get_position(db, sender_id)
                message = data["content"]["message"]
                if sender_id == userid:
                    return
                if position is not None:
                    u_lat = position[0]
                    u_lon = position[1]
                    m_lat = sender_position[0]
                    m_lon = sender_position[1]
                    m_radius = data["radius"]
                    if abs(u_lat - m_lat) < m_radius and abs(u_lon - m_lon) < m_radius:
                        content = {"time": strftime("%Y-%m-%d %H:%M:%S", gmtime()), "from": sender_id, "text": message}
                        sio.emit("user:incoming", content, room=room_id)
                else:
                    sio.emit("error", {"error": "User has no position, please set the position first"}, room=room_id)

            queue.configure_consume(channel, user_queue_callback, queue_id)

            # Bot2user messages
            queue_name = Queues.USER_B2U_PREFIX + "_" + str(userid) + "_" + uuid.uuid4().hex
            queue_id = queue.create_queue(channel, queue_name)
            # This queue is, by default, not binded to any exchange, as the routing key depends on the location
            # Will be handy when reconfiguring the building
            self.channels_dict[request.sid]["bot_queue"] = queue_id

            def bot_queue_callback(ch, method, properties, body):
                print(ch, body, properties, method)
                # Here messages already are filtered by the exchange
                emit("bot:incoming", body)

            queue.configure_consume(channel, bot_queue_callback, queue_id)
            thread = Thread(target=queue.start_message_consumption, args=(channel,))
            thread.start()
            emit("handshake_allowed", {"success": "true", "room": userid})
            print("Succesful handshake with " + userid, "At:" + thread.name)

        @sio.on("disconnect")
        def disconnect_handler():
            # Here disconnect the queue based on the request sid, by closing the channel opened in the handshake
            if request.sid in self.channels_dict:
                self.channels_dict[request.sid]["channel"].close()
                self.channels_dict[request.sid]["connection"].close()
                db = self.channels_dict[request.sid]["db"].close()
                clear_position(db, self.channels_dict[request.sid]["user_id"])
                self.channels_dict[request.sid]["db"].close()

            # Pop from dictionary
            self.channels_dict.pop(request.sid)

        @sio.on("building_change")
        def building_change_handler(json_data):
            data = json_engine.loads(json_data)
            # Get bot queue
            if request.sid not in self.channels_dict:
                #  User not authenticated
                emit('error', {'error': 'User not authenticated'})
                disconnect()
                return
            bqueue = self.channels_dict[request.sid]["bot_queue"]
            channel = self.channels_dict[request.sid]["channel"]
            user = self.channels_dict[request.sid]["user_id"]
            # Store location in db
            try:
                db = self.channels_dict[request.sid]["db"]
                set_position(db, user, data["body"]["lat"], data["body"]["lon"])
                # Query building
                building = get_user_building(db, user)
                # Unbind from old building
                # Bind to new building
                queue.rebind_queue(channel, bqueue, configs.BOTS_EXCHANGE, building)
                if building is None:
                    building = "Outside"
                emit("building_change_success", {"building": building, "success": "yes"})

            except TypeError as e:
                print("Error in change building request: " + str(e))
                emit('error', {'error': 'Error in change building request'})

        @sio.on_error()
        def error(e):
            print(e, request.sid)

        return sio
