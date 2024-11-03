from flask import Flask, render_template
from flask import abort as flask_abort
from flask_socketio import SocketIO
from flask import request, session
from flask import make_response
from random import randrange
from game import PongGame

# Flask App initialisieren
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# this class handles the user sessions
class UserSessions:
    def __init__(self):
        self.all_user_sessions = {}

    def create_user_session(self):
        # create random number
        session_id = randrange(start=100000,stop=1000000)
        return session_id
    
    def number_of_sessions(self):
        return len(self.all_user_sessions.keys())

# movement from players
@socketio.on('move')
def handle_move(data):
    current_game.game_move(data)

# frontend
@app.route('/')
def index():
    # identify if this user is already "logged" in
    if not request.cookies.get("sid"):
        sid = user_session.create_user_session()
    else:
        sid = request.cookies.get("sid")

    if len(user_session.all_user_sessions.keys()) <= 2:
        # find out if the client is already connected or not
        if sid in user_session.all_user_sessions.values():
            pass
        else:
            if 'player1' not in user_session.all_user_sessions:
                user_session.all_user_sessions['player1'] = sid
            elif 'player2' not in user_session.all_user_sessions:
                user_session.all_user_sessions['player2'] = sid
            else:
                flask_abort(401, "Maximum amount of Players reached!")
        
        # return the identifier to the client
        session['sid'] = sid
        resp = make_response(render_template('index.html'))
        resp.set_cookie("sid", str(sid))
        return resp
    else:
        flask_abort(401, "Maximum amount of Players reached!")

# start the game in the background
@socketio.on('connect')
def start_game_loop():
    sid = request.cookies.get("sid")
    session['sid'] = sid
    socketio.start_background_task(game_loop)

# remove players when they are gone.
@socketio.on('disconnect')
def on_disconnect():
    sid = request.cookies.get("sid")
    if sid == user_session.all_user_sessions.get('player1'):
        del user_session.all_user_sessions['player1']
    elif sid == user_session.all_user_sessions.get('player2'):
        del user_session.all_user_sessions['player2']

def game_loop():
    while True:
        # 30 milisecond buffer
        current_game.update()

# start the game
if __name__ == '__main__':
    user_session = UserSessions()
    current_game = PongGame(socketio, user_session, session)
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    