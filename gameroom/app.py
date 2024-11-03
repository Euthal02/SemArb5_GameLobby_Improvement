import pygame
from flask import Flask, render_template
from flask import abort as flask_abort
from flask_socketio import SocketIO
from flask import request, session
from flask import make_response
from random import randrange

# Flask App initialisieren
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Pygame initialisieren (im Hintergrund)
pygame.init()

# Spielfenster-Einstellungen
WIDTH, HEIGHT = 800, 600
# Hintergrund
WHITE = (255, 255, 255)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20
# Basis Einstellungen
paddle_speed = 6.5
ball_speed_x, ball_speed_y = 3.5, 3.5

# Spieler- und Ball-Einstellungen
# // bedeutet Division ohne Rest
player1 = pygame.Rect(10, ((HEIGHT//2)-(PADDLE_HEIGHT//2)), PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect((WIDTH-20), ((HEIGHT//2)-(PADDLE_HEIGHT//2)), PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(((WIDTH//2)-(BALL_SIZE//2)), ((HEIGHT//2)-(BALL_SIZE//2)), BALL_SIZE, BALL_SIZE)

# Spieler-ID-Tracking
clients = {}

# this class handles the user sessions
class UserSessions:
    def __init__(self):
        self.all_user_sessions = {}

    def create_user_session(self):
        # create random number
        session_id = randrange(start=100000,stop=1000000)

        # add session
        player_number = self.number_of_sessions() + 1
        self.all_user_sessions[session_id] = player_number

        return session_id
    
    def number_of_sessions(self):
        return len(self.all_user_sessions.keys())
    
    def get_player(self, provided_id):
        return self.all_user_sessions.get(provided_id)

# Spielzustand aktualisieren
def update_game():
    global ball_speed_x, ball_speed_y

    # Ballbewegung
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Kollisionen mit Wänden
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    # Kollision mit Spieler Paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
    
    # Ball zurücksetzen, wenn er das Spielfeld verlässt
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2

    # Spielzustand an den Client senden
    socketio.emit('update', {
        'ball': {'x': ball.x, 'y': ball.y},
        'player1': {'x': player1.x, 'y': player1.y},
        'player2': {'x': player2.x, 'y': player2.y}
    })

# Websocket für Spielersteuerung
@socketio.on('move')
def handle_move(data):
    sid = session.get('sid')
    if sid == clients.get('player1') and data['direction']:
        if data['direction'] == 'up' and player1.top > 0:
            player1.y -= paddle_speed
        elif data['direction'] == 'down' and player1.bottom < HEIGHT:
            player1.y += paddle_speed
    elif sid == clients.get('player2') and data['direction']:
        if data['direction'] == 'up' and player2.top > 0:
            player2.y -= paddle_speed
        elif data['direction'] == 'down' and player2.bottom < HEIGHT:
            player2.y += paddle_speed

# HTML-Seite laden (Frontend)
@app.route('/')
def index():
    if not request.cookies.get("sid"):
        sid = user_session.create_user_session()
    else:
        sid = request.cookies.get("sid")

    print(sid)
    print(clients)

    if len(clients.keys()) <= 2:
        if sid in clients.values():
            pass
        else:
            if 'player1' not in clients:
                clients['player1'] = sid
            elif 'player2' not in clients:
                clients['player2'] = sid
            else:
                flask_abort(401, "Maximum amount of Players reached!")
        session['sid'] = sid

        resp = make_response(render_template('index.html'))
        resp.set_cookie("sid", str(sid))
        return resp
    else:
        flask_abort(401, "Maximum amount of Players reached!")

# Hauptspiel-Schleife als Hintergrund-Task starten
@socketio.on('connect')
def start_game_loop():
    sid = request.cookies.get("sid")
    session['sid'] = sid
    socketio.start_background_task(game_loop)

@socketio.on('disconnect')
def on_disconnect():
    sid = request.cookies.get("sid")
    if sid == clients.get('player1'):
        del clients['player1']
    elif sid == clients.get('player2'):
        del clients['player2']

# Hauptspiel-Schleife
def game_loop():
    while True:
        pygame.time.delay(30)  # Verzögerung für FPS
        update_game()

# Server starten
if __name__ == '__main__':
    # create a storage for the user sessions
    global user_session
    user_session = UserSessions()

    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
