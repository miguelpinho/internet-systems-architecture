from DbClient.db import get_db
from .message_queues import *
from Utils.consts import Queues
from DbInterface import logs
from threading import Thread
import json as json_engine


def create_logs_queues(private_consts):
    # Created in a background thread due to the synchronous behaviour of message queues
    thread = Thread(target=queues_creator, args=(private_consts,))
    thread.start()


def queues_creator(private_consts):
    # Connect to the DB
    db = get_db(private_consts)

    # Connect to the message queue broker
    connection = connect(private_consts.Queues.QUEUE_HOST)
    channel = create_channel(connection)

    # Define the message queue callbacks
    def user_message_logs_callback(channel, method, properties, body):
        data = json_engine.loads(body)
        sender_id = data["content"]["user_id"]
        message = data["content"]["message"]
        logs.store_msg_user(db, ist_id=sender_id, msg=message)

    def bots_message_logs_callback(channel, method, properties, body):
        data = json_engine.loads(body)
        message = data["text"]
        bot_id = int(data["building"])
        logs.store_msg_building(db, bid=bot_id, msg=message)

    # Create bots2user message queue - The routing key "#" configures the queue to receive all messages
    queue_id = create_queue(channel, "logs_queue_bots_exchange")
    bind_queue(channel, queue_id, Queues.BOTS_EXCHANGE, "#")
    configure_consume(channel, bots_message_logs_callback, queue_id)

    # Create user2user message queue
    queue_id = create_queue(channel, "logs_queue_user_exchange")
    bind_queue(channel, queue_id, Queues.USER_EXCHANGE)
    configure_consume(channel, user_message_logs_callback, queue_id)

    start_message_consumption(channel)
