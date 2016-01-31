import json
import redis


class Control(object):

    def __init__(self):
        self.queue = redis.Redis()

    def player_connected(self, player):
        data = json.dumps(player)
        self.queue.rpush('player_connected', data)

    def player_disconnected(self, player):
        data = json.dumps(player)
        self.queue.rpush('player_disconnected', data)

    def player_move(self, data):
        movement = json.loads(data)
        self.queue.rpush('player_move', movement)

    def send(self, message):
        # {"type":"humitos","data":{"type":"startx","value":458}}

        # README: we need to send the data as JSON string and then
        # convert to dictionary from the pilas-engine
        # Actor.actualizar() method
        nickname = json.loads(message)['type']
        self.queue.rpush(nickname, message)
