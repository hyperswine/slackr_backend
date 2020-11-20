'''
Sets the routes for /message/.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from message_route.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
missing-function-docstring:
    Since the route functions are extremely self explanatory and simply act as communication with
    the frontend, there is no need for function docstrings.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

from json import dumps
import datetime
from flask import Blueprint, request

import app.message as message

MOD_MESSAGE = Blueprint('message', __name__)

@MOD_MESSAGE.route('/send', methods=["POST"])
def msg_send():
    data = request.get_json()
    return dumps(message.send(data['token'], int(data['channel_id']), data['message']))

@MOD_MESSAGE.route('/sendlater', methods=["POST"])
def msg_send_later():
    data = request.get_json()
    time_to_send = datetime.datetime.utcfromtimestamp(data['time_sent'])
    return dumps(message.send_later(data['token'], int(data['channel_id']), data['message'], time_to_send))

@MOD_MESSAGE.route('/react', methods=["POST"])
def msg_react():
    data = request.get_json()
    message.react(data['token'], int(data['message_id']), data['react_id'])
    return dumps({})

@MOD_MESSAGE.route('/unreact', methods=["POST"])
def msg_unreact():
    data = request.get_json()
    message.unreact(data['token'], int(data['message_id']), data['react_id'])
    return dumps({})

@MOD_MESSAGE.route('/pin', methods=["POST"])
def msg_pin():
    data = request.get_json()
    message.pin(data['token'], int(data['message_id']))
    return dumps({})

@MOD_MESSAGE.route('/unpin', methods=["POST"])
def msg_unpin():
    data = request.get_json()
    message.unpin(data['token'], int(data['message_id']))
    return dumps({})

@MOD_MESSAGE.route('/remove', methods=["DELETE"])
def msg_remove():
    data = request.get_json()
    message.remove(data['token'], int(data['message_id']))
    return dumps({})

@MOD_MESSAGE.route('/edit', methods=["PUT"])
def msg_edit():
    data = request.get_json()
    message.edit(data['token'], int(data['message_id']), data['message'])
    return dumps({})
