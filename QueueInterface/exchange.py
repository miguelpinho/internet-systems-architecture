from .message_queues import connect, create_channel, create_exchange
from Utils.consts import Queues


def create_exchanges(private_consts):
    connection = connect(private_consts)
    channel = create_channel(connection)
    create_exchange(channel, Queues.BOTS_EXCHANGE, "topic")
    create_exchange(channel, Queues.USER_EXCHANGE, "fanout")
    channel.close()
    connection.close()
