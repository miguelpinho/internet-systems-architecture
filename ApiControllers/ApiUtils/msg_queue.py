from flask import g
from QueueInterface import message_queues as queue_adapter


def get_queue(private_consts):
    if 'queue' not in g:
        g.db = queue_adapter.connect(private_consts)
    return g.db
