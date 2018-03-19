from flask_socketio import SocketIO

socket_io = SocketIO()


@socket_io.on('message')
def handle_message(message):
    print('received message: ' + message)


@socket_io.on('json')
def handle_json(json):
    print('received json: ' + str(json))
