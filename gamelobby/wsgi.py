from app import create_lobby

app, socketio_object = create_lobby()

if __name__ == "__main__":
    socketio_object.run(app, host="0.0.0.0", port=80, debug=True)