import redis
import json

from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

r = redis.Redis()


@sockets.route('/echo')
def echo_socket(ws):
    print('Connected.')
    while True:
        message = ws.receive()
        # print(message)
        data = json.loads(message)['data']
        r.rpush(data['type'], data['value'])


@app.route('/')
def hello():
    return 'Hello World!'
