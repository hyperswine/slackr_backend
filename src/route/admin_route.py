'''
Sets the routes for /admin/.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from admin_route.py, but we run the server from server.py, there will be
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

import app.admin as admin

MOD_ADMIN = Blueprint('admin', __name__)

###################
## ADMIN ROUTES
###################


@MOD_ADMIN.route('/userpermission/change', methods=["POST"])
def admin_change():
    data = request.get_json()
    return dumps(admin.change_permissions(data["token"], data["u_id"], data["permission_id"]))


@MOD_ADMIN.route('/user/remove', methods=["DELETE", "POST"])
def admin_remove():
    data = request.get_json()
    return dumps(admin.remove_user(data["token"], data["u_id"]))
