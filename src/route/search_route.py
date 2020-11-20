'''
Sets the route for /search only.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from search_route.py, but we run the server from server.py, there will be
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

import app.search as search

MOD_SEARCH = Blueprint('search', __name__)

# Note: No URL prefix for this route.
@MOD_SEARCH.route('/search', methods=["GET"])
def search_():
    return dumps(search.search(request.args.get("token"), request.args.get("query_str")))
    