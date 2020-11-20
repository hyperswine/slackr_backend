'''
Sets the routes for /channels/.

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

import app.channels as channels

MOD_CHANNELS = Blueprint('channels', __name__)

@MOD_CHANNELS.route('/list', methods=["GET"])
def chs_list():
    return dumps(channels.list_(request.args.get('token')))


@MOD_CHANNELS.route('/listall', methods=["GET"])
def chs_listall():
    return dumps(channels.listall(request.args.get('token')))


@MOD_CHANNELS.route('/create', methods=["POST"])
def chs_create():
    data = request.get_json()
    return dumps(channels.create(data['token'], data['name'], data['is_public']))
