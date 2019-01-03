import math

from flask import Flask, request, g
from flask_socketio import SocketIO, emit

from DbInterface.user import get_userid_from_cookie, clear_position, set_position, get_user_building, get_position
from db import get_db
from QueueInterface import message_queues as queue

from Utils.consts import Queues as configs


class Sockio:

    def __init__(self, private_consts):
        self.connection = queue.connect(private_consts)
        self.consts = private_consts
        self.channels_dict = {}

    def config_socketio(self, flask_app: Flask):
        sio = SocketIO(app=flask_app)

        @sio.on("handshake")
        def handshake(json):
            """The handshake process matches the user and the socketio session
            Through this process the message queues for that user are declared and the consumption of messages is started
            """

            # json object contains the session cookie, thus identifying the sender
            # Handshake the request sid with the user identifier, through the json[data] cookie
            # get_cache(cookie) -> if there is proceed and get userid from the cache
            userid = get_userid_from_cookie(json["data"])
            if userid is None:
                emit('error', {'error': 'User not authenticated'})
                #  disconnect()
                #  return

            # Create message queue use this context emit to send messages
            channel = queue.create_channel(self.connection)

            self.channels_dict[request.sid] = {"channel": channel, "user_id": userid}

            # User2user messages
            queue_id = queue.create_queue(channel)
            # Bind to fanout type user exchange
            queue.bind_queue(channel, queue_id, configs.USER_EXCHANGE)

            def user_queue_callback(ch, method, properties, body):
                print(ch, body, properties, method)
                # Here filter messages by userid, only emit the ones corresponding to this user
                # if userlocation ~= messagelocation -> emit the message
                # Get user location
                db = get_db(private_consts)
                position = get_position(db, userid)
                if position is not None:
                    u_lat = position["lat"]
                    u_lon = position["lon"]
                    # TODO: Get lat, lon and radius from message
                    m_lat = 0
                    m_lon = 0
                    m_radius = 0
                    if abs(u_lat-m_lat) < m_radius and abs(u_lon-m_lon) < m_radius:
                        emit("user:incoming", body)
                else:
                    emit("error", {"error": "User has no position, please set the position first"})

            queue.configure_consume(channel, user_queue_callback, queue_id)

            # Bot2user messages
            queue_id = queue.create_queue(channel)
            # This queue is, by default, not binded to any exchange, as the routing key depends on the location
            # Will be handy when reconfiguring the building
            self.channels_dict[request.sid]["bot_queue"] = queue_id

            def bot_queue_callback(ch, method, properties, body):
                print(ch, body, properties, method)
                # Here messages already are filtered by the exchange
                emit("bot:incoming", body)

            queue.configure_consume(channel, bot_queue_callback, queue_id)
            queue.start_message_consumption(channel)

        @sio.on("disconnect")
        def disconnect():
            # TODO: Activate when db, cache and exchange are complete
            # Here disconnect the queue based on the request sid, by closing the channel opened in the handshake
            if request.sid in self.channels_dict:
                self.channels_dict[request.sid]["channel"].close()
            db = get_db(private_consts)
            # clear_position(db, self.channels_dict[request.sid]["user_id"])
            # Pop from dictionary
            self.channels_dict.pop(request.sid)

        @sio.on("building_change")
        def building_change(json):
            # TODO: Activate when db, cache and exchange are complete
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
            db = get_db(private_consts)
            #  set_position(db, user, json["data"]["lat"], json["data"]["lon"])
            # Query building
            #  building = get_user_building(db, user)

            # Unbind from old building
            # Bind to new building
            # queue.rebind_queue(channel, bqueue, configs.BOTS_EXCHANGE, building)
            # TODO: Send success response to client
            emit("building_change_success", {"building": "some building", "success": "yes"})

        @sio.on_error()
        def error(e):
            print(e, request.sid)

        return sio
