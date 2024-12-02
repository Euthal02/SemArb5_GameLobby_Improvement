from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect
from app.game_update import update_game, get_random_ball_speed

# Game state
game_state = {
    # ball speed should be random
    "ball": {"x": 300, "y": 200, "dx": get_random_ball_speed(), "dy": get_random_ball_speed()},
    "paddles": {"player1": 160, "player2": 160},
    "scores": {"player1": 0, "player2": 0},
    "width": 700,
    "height": 500,
    "paddle_height": 90,
    "paddle_width": 10,
}

players = {}

def reset_game_scores(game_state_dict=game_state):
    game_state_dict["scores"] = {"player1": 0, "player2": 0}


def setup_game():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app, send_wildcard=True)

    # this just returns the basic index.html
    @app.route("/")
    def index():
        return render_template("game.html")
    
    @app.route('/health')
    def health():
        return "OK", 200
    
    @app.route("/player_count")
    def player_count():
        return jsonify({"player_count": len(players.keys())})

    socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

    @socketio.on("connect")
    def on_connect():
        global players
        if len(players.keys()) < 2:
            if 1 not in players.values():
                player_id = 1
            else:
                player_id = 2

            players[request.sid] = player_id
            # the room parameter just defines the scope of this reply.
            emit("player_id", player_id, room=request.sid)
            print(f"Player {player_id} connected: {request.sid}")
        else:
            disconnect()

    @socketio.on("disconnect")
    def on_disconnect():
        global players
        if request.sid in players.keys():  
            print(f"Player {players[request.sid]} disconnected: {request.sid}")
            del players[request.sid]

    @socketio.on("move_paddle")
    def move_paddle(data):
        player = data["player"]
        position = data["position"]

        # update the paddles
        game_state["paddles"][player] = max(0, min(game_state["height"] - game_state["paddle_height"], position))

    # Background game loop
    def game_loop():
        ongoing_game = False
        while True:
            if len(players.keys()) == 2:
                if ongoing_game:
                    update_game(game_state_dict=game_state, socketio_object=socketio)
                else:
                    ongoing_game = True
                    reset_game_scores(game_state_dict=game_state)
                    update_game(game_state_dict=game_state, socketio_object=socketio)
            else:
                pass

            socketio.sleep(0.03)  # 30 FPS

    socketio.start_background_task(game_loop)

    return app, socketio
