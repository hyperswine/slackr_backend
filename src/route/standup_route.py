'''
Sets the routes for /standup/.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from standup_route.py, but we run the server from server.py, there will be
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
import app.standup as st

MOD_STANDUP = Blueprint('standup', __name__)

@MOD_STANDUP.route('/start', methods=["POST"])
def st_start():
    data = request.get_json()
    return dumps(st.start(data["token"], int(data["channel_id"]), data["length"]))


@MOD_STANDUP.route('/active', methods=["GET"])
def st_active():
    return dumps(st.active(request.args.get("token"), int(request.args.get("channel_id"))))

@MOD_STANDUP.route('/send', methods=["POST"])
def st_send():
    data = request.get_json()
    return dumps(st.send(data["token"], int(data["channel_id"]), data["message"]))
