'''
Sets the routes for /profileimages/.

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
from flask import Blueprint, send_file

import app.admin as admin

MOD_PROFILEIMAGES = Blueprint('profileimages', __name__)

###################
## PROFILEIMAGES ROUTES
###################


@MOD_PROFILEIMAGES.route('/<var>', methods=["GET"])
def get_img(var):
    return send_file(f'../profile_images/{var}', mimetype='image/jpg')
