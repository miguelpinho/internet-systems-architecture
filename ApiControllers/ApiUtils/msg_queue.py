import pika
from flask import g, current_app
from QueueInterface import message_queues as queue_adapter
from Utils.consts import Queues


def get_queue_connection():
    if 'q_connection' not in g:
        g.q_connection = queue_adapter.connect(current_app.private_consts.Queues.QUEUE_HOST)
    return g.q_connection


def get_queue_channel(connection):
    if 'q_channel' not in g:
        g.q_channel = queue_adapter.create_channel(connection)
    return g.q_channel


def publish_user_message(channel, message):
    channel.basic_publish(exchange=Queues.USER_EXCHANGE,
                          routing_key='',
                          body=message)


def publish_bot_message(channel, bid, message):
    channel.basic_publish(exchange=Queues.BOTS_EXCHANGE,
                          routing_key=bid,
                          body=message)
