'''
Sets the routes for /users/all only.

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

import app.user as user

MOD_USERS = Blueprint('users', __name__)

@MOD_USERS.route('all', methods=["GET"])
def users_all():
    return dumps(user.all_(request.args.get("token")))
