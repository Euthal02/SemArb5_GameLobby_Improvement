from app import setup_game

app, socketio_object = setup_game()

if __name__ == '__main__':
    socketio_object.run(app, host="0.0.0.0", port=5000, debug=True)
