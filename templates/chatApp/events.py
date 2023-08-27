from flask_socketio import emit
from .extension import socketio
from reply import reply


@socketio.on('message')
def handle_message(message):
    response = reply(message)
    emit("response", {"message": response})
