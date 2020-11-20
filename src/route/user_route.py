'''
Sets the routes for /user/.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from user_route.py, but we run the server from server.py, there will be
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

MOD_USER = Blueprint('user', __name__)

@MOD_USER.route('/profile/setname', methods=["PUT"])
def user_setname():
    data = request.get_json()
    return dumps(user.setname(data["token"], data["name_first"], data["name_last"]))



@MOD_USER.route('/profile/setemail', methods=["PUT"])
def user_setemail():
    data = request.get_json()
    return dumps(user.setemail(data["token"], data["email"]))


@MOD_USER.route('/profile/sethandle', methods=["PUT"])
def user_sethandle():
    data = request.get_json()
    return dumps(user.sethandle(data["token"], data["handle_str"]))


@MOD_USER.route('/profile', methods=["GET"])
def user_profile():
    return dumps(user.profile(request.args.get("token"), int(request.args.get("u_id"))))


@MOD_USER.route('/profile/uploadphoto', methods=["POST"])
def user_uploadphoto():
    data = request.get_json()
    return dumps(user.upload_photo(data['token'], data['img_url'], data['x_start'], data['y_start'], data['x_end'],\
                                   data['y_end']))
