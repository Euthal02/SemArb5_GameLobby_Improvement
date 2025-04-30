from random import choice as rand_choice

def update_game(game_state_dict, socketio_object):
    ball = game_state_dict["ball"]
    paddles = game_state_dict["paddles"]

    # Move ball
    ball["x"] += ball["dx"]
    ball["y"] += ball["dy"]

    # Ball collision with top/bottom walls
    if ball["y"] <= 0 or ball["y"] >= game_state_dict["height"]:
        ball["dy"] *= -1

    # Ball collision with paddles
    if ball["x"] <= game_state_dict["paddle_width"]:
        # wenn sich die y position zwischen dem bottom und der top des paddles befindet,
        # wird die geschwindigkeit reversed
        if paddles["player1"] <= ball["y"] <= paddles["player1"] + game_state_dict["paddle_height"]:
            ball["dx"] *= -1
        else:
            game_state_dict["scores"]["player2"]["score"] += 1
            game_state_dict = reset_ball(game_state_dict)
    elif ball["x"] >= game_state_dict["width"] - game_state_dict["paddle_width"]:
        if paddles["player2"] <= ball["y"] <= paddles["player2"] + game_state_dict["paddle_height"]:
            ball["dx"] *= -1
        else:
            game_state_dict["scores"]["player1"]["score"] += 1
            game_state_dict = reset_ball(game_state_dict)

    # Broadcast game state to all clients
    socketio_object.emit("game_state", game_state_dict)

def get_random_ball_speed():
    return rand_choice([-8, -7, -6, -5, 5, 6, 7, 8])

def reset_ball(game_state_dict):
    game_state_dict["ball"] = {
        "x": game_state_dict["width"] // 2,
        "y": game_state_dict["height"] // 2,
        "dx": get_random_ball_speed(),
        "dy": get_random_ball_speed(),
    }
    return game_state_dict
