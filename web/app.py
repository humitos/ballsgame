from control import Control
from flask import Flask, render_template, redirect, url_for, request
from flask_sockets import Sockets

# To get WebSocket support we need to run it as:
#    gunicorn -k flask_sockets.worker -b 0.0.0.0:5000 app:app
#
# For development purpose only (without ws support):
#    python app.py

app = Flask(__name__)
sockets = Sockets(app)
control = Control()

PLAYERS = []


@sockets.route('/joystick')
def joystick(ws):
    # control.player_connected(player)
    while True:
        message = ws.receive()
        control.send(message)
    # control.player_disconnected(player)


@app.route('/register', methods=['POST'])
def register():
    ip = request.remote_addr
    color = 'green'

    # TODO: check the nickname choosen is not registered yet
    nickname = request.form['nickname']

    player = {
        'color': color,
        'nickname': nickname,
        'ip': ip,
    }
    PLAYERS.append(player)
    return redirect(url_for('play', nickname=nickname))


@app.route('/play/<nickname>/')
def play(nickname):
    context = {
        # FIXME: use the same host/port than Flask server
        'host': 'victoria.redlibre',
        'port': 5000,
        'nickname': nickname,
    }
    return render_template('play.html', **context)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
