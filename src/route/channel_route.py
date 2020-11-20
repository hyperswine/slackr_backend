'''
Sets the routes for /channel/.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from channel_route.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
missing-function-docstring:
    Since the route functions are extremely self explanatory and simply act as communication with
    the frontend, there is no need for function docstrings.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=missing-function-docstring

from json import dumps
from flask import Blueprint, request

import app.channel as ch

MOD_CHANNEL = Blueprint('channel', __name__)

@MOD_CHANNEL.route('/invite', methods=["POST"])
def ch_inv():
    data = request.get_json()
    return dumps(ch.inv(data["token"], int(data["channel_id"]), int(data["u_id"])))


@MOD_CHANNEL.route('/details', methods=["GET"])
def ch_det():
    return dumps(ch.det(request.args.get("token"), int(request.args.get("channel_id"))))


@MOD_CHANNEL.route('/messages', methods=["GET"])
def ch_msg():
    return dumps(ch.msg(request.args.get('token'), int(request.args.get('channel_id')), \
        int(request.args.get('start'))))


@MOD_CHANNEL.route('/leave', methods=["POST"])
def ch_lev():
    data = request.get_json()
    print(data)
    return dumps(ch.lev(data["token"], int(data["channel_id"])))


@MOD_CHANNEL.route('/join', methods=["POST"])
def ch_joi():
    data = request.get_json()
    return dumps(ch.joi(data["token"], int(data["channel_id"])))


@MOD_CHANNEL.route('/addowner', methods=["POST"])
def ch_add():
    data = request.get_json()
    return dumps(ch.add_owner(data["token"], int(data["channel_id"]), data["u_id"]))


@MOD_CHANNEL.route('/removeowner', methods=["POST"])
def ch_rem():
    data = request.get_json()
    return dumps(ch.rem_owner(data["token"], int(data["channel_id"]), data["u_id"]))
