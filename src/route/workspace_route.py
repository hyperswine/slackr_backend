'''
Sets the routes for /workspace/reset only.

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
from flask import Blueprint

import app.workspace as workspace

MOD_WORKSPACE = Blueprint('workspace', __name__)

@MOD_WORKSPACE.route('/reset', methods=["POST"])
def wks_reset():
    workspace.workspace_reset()
    return dumps({})
