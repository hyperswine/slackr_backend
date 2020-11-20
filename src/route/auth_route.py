'''
Sets the routes for /auth/.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from auth_route.py, but we run the server from server.py, there will be
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

import app.auth as auth


MOD_AUTH = Blueprint('auth', __name__)


@MOD_AUTH.route('/register', methods=["POST"])
def auth_register():
    data = request.get_json()
    return dumps(auth.register(data["email"], data["password"], data["name_first"], \
        data["name_last"]))


@MOD_AUTH.route('/login', methods=["POST"])
def auth_login():
    data = request.get_json()
    return dumps(auth.login(data["email"], data["password"]))


@MOD_AUTH.route('/logout', methods=["POST"])
def auth_logout():
    data = request.get_json()
    return dumps(auth.logout(data["token"]))


@MOD_AUTH.route('/passwordreset/request', methods=["POST"])
def auth_request():
    data = request.get_json()
    return dumps(auth.passwordreset_request(data["email"]))


@MOD_AUTH.route('/passwordreset/reset', methods=["POST"])
def auth_reset():
    data = request.get_json()
    return dumps(auth.passwordreset_reset(data["reset_code"], data["new_password"]))