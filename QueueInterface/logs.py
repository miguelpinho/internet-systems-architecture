from DbClient.db import get_db
from .message_queues import *
from Utils.consts import Queues
from DbInterface import logs
from threading import Thread


def create_logs_queues(private_consts):
    thread = Thread(target=queues_creator, args=(private_consts,))
    thread.start()


def queues_creator(private_consts):
    # Connect to the DB TODO: Pass info for connection
    db = get_db()

    # Connect to the message queue broker
    connection = connect(private_consts.Queues.QUEUE_HOST)
    channel = create_channel(connection)

    # Define the message queue callbacks
    def user_message_logs_callback(channel, method, properties, body):
        logs.store_msg_user(db, ist_id="some id", msg="some message")

    def bots_message_logs_callback(channel, method, properties, body):
        logs.store_msg_building(db, bid="some bid", msg="some message")

    # Create bots2user message queue - The routing key "#" configures the queue to receive all messages
    queue_id = create_queue(channel)
    bind_queue(channel, queue_id, Queues.BOTS_EXCHANGE, "#")
    configure_consume(channel, bots_message_logs_callback, queue_id)

    # Create user2user message queue
    queue_id = create_queue(channel)
    bind_queue(channel, queue_id, Queues.USER_EXCHANGE)
    configure_consume(channel, user_message_logs_callback, queue_id)

    start_message_consumption(channel)
