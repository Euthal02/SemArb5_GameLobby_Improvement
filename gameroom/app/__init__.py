from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect
from app.game_update import update_game, get_random_ball_speed

# Game state
game_state = {
    # ball speed should be random
    "ball": {"x": 300, "y": 200, "dx": get_random_ball_speed(), "dy": get_random_ball_speed()},
    "paddles": {"player1": 160, "player2": 160},
    "scores": {"player1": {"score": 0, "username": None}, "player2": {"score": 0, "username": None}},
    "width": 700,
    "height": 500,
    "paddle_height": 90,
    "paddle_width": 10,
}

players = {}

def reset_game_scores(game_state_dict=game_state):
    game_state_dict["scores"] = {"player1": {"score": 0, "username": None}, "player2": {"score": 0, "username": None}}


def setup_game():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    CORS(app, send_wildcard=True)
    socketio = SocketIO(app, async_mode="eventlet")

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

    @socketio.on("connect")
    def on_connect():
        global players
        socketio.start_background_task(game_loop)
        if len(players.keys()) < 2:
            if len(players.keys()) == 1:
                # since this section can only be reached if there is only one player.
                # i can safely assume that either the id 1 is already used, or not, in which case we use the id 1.
                player_id = 2
                for individual_player in players.keys():
                    if 1 not in players[individual_player].values():
                        player_id = 1
            else:
                player_id = 1

            players[request.sid]= {"playerId": player_id}
            # the room parameter just defines the scope of this reply.
            emit("player_id", player_id, room=request.sid)
        else:
            disconnect()

    @socketio.on("disconnect")
    def on_disconnect():
        global players
        if request.sid in players.keys():
            del players[request.sid]

    @socketio.on("move_paddle")
    def move_paddle(data):
        player = data["player"]
        position = data["position"]

        # update the paddles
        game_state["paddles"][player] = max(0, min(game_state["height"] - game_state["paddle_height"], position))

    @socketio.on("update_username")
    def update_username(data):
        if request.sid in players.keys():
            username = data["username"]
            players[request.sid]["username"] = username
            game_state["scores"][f"player{players[request.sid]["playerId"]}"]["username"] = username

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

    return app, socketio
