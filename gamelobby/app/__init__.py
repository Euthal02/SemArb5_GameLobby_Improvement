from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

players = {}  # Speichert Spielerinformationen

def create_lobby():
    app = Flask(__name__)
    CORS(app, send_wildcard=True)
    socketio = SocketIO(app, cors_allowed_origins="*")

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @socketio.on("connect")
    def connect():
        socketio.start_background_task(update_scoreboard)

    @socketio.on("join_lobby")
    def join_lobby(data):
        name = data["name"]
        players[request.sid] = {"name": name, "score": 0}

    @socketio.on("join_game")
    def join_game(data):
        print(data)
        print(players)
        # ToDo: implement logic for passing the username

    @socketio.on("disconnect")
    def disconnect():
        players.pop(request.sid, None)

    # @socketio.on("update_score")
    # def update_score(data):
    #     if request.sid in players:
    #         players[request.sid]["score"] = data["score"]
    #     emit("update_players", list(players.values()), broadcast=True)

    # Background scoreboard loop
    def update_scoreboard():
        while True:
            players_list = []
            if len(players.keys()) >= 1:
                for player in players.keys():
                    players_list.append({"name": players[player]["name"], "score": players[player]["score"]})
                socketio.emit("update_scoreboard", players_list)
            else:
                pass

            socketio.sleep(0.03)

    return app, socketio
