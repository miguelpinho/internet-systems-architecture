import pika


def connect(private_consts):
    return pika.BlockingConnection(pika.connection.URLParameters(private_consts.Queues.QUEUE_HOST))


def create_channel(connection):
    channel = connection.channel()
    return channel


def create_queue(channel):
    result = channel.queue_declare(auto_delete=True)
    return result.method.queue


def bind_queue(channel, queue_id, exchange):
    channel.queue_bind(queue=queue_id, exchange=exchange)


def rebind_queue(channel, queue_id, exchange, routing_key):
    channel.queue_unbind(queue=queue_id, exchange=exchange)
    channel.queue_bind(queue=queue_id, exchange=exchange, routing_key=routing_key)


def configure_consume(channel, queue_callback, queue_id):
    channel.basic_consume(queue_callback, queue=queue_id, no_ack=True)


def start_message_consumption(channel):
    channel.start_consuming()


def create_exchange(channel, exchange_name, exchange_type):
    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
