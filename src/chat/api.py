from flask import Blueprint, render_template
from flask_socketio import SocketIO
from utils import login_required
from loguru import logger

socket_blueprint = Blueprint('socket', __name__)
socketio = SocketIO(async_mode='gevent', engineio_logger=True)


@socket_blueprint.route('/')
@login_required
def index():
    return render_template('chat.html')


@socketio.on('connect', namespace='/socket')
def handle_connect():
    logger.success('Client connected')


# @socketio.on('disconnect', namespace='/socket')
# def handle_disconnect():
#     logger.success('Client disconnected')
#
#
@socketio.on('message', namespace='/socket')
def handle_message(data):
    logger.success('Received message:', data)
    socketio.emit('message', data, namespace='/socket')
