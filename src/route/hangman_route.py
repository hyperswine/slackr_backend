'''
Sets the routes for /hangman/.

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

import app.hangman as hangman

MOD_HANG = Blueprint('hangman', __name__)

@MOD_HANG.route('/start', methods=["POST"])
def hang_start():
    data = request.get_json()
    return dumps(hangman.start(data['token'], int(data['channel_id']), data['wordX']))


@MOD_HANG.route('/guess', methods=["POST"])
def hang_guess():
    data = request.get_json()
    return dumps(hangman.guess(data['token'], int(data['channel_id']), data['wordY']))
