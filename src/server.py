'''
Where the server is housed. Execute this to run the server.

Pylint disable justifications:
missing-function-docstring:
    Most of the code in this file is provided by the spec. Hence, no additional explanations will
    be added.
    In addition, most of the cost is self-explanatory.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=missing-function-docstring
import sys
import time
from json import dumps
from flask import request
from flask_cors import CORS
from main.error import InputError
from main.app_ import APP
from main.pickle_ import pickle_data
from app.message import check_pending_messages
import app.bot as bot


def defaultHandler(err):  # pylint: disable=invalid-name
    # (provided function, will ignore pylint errors)
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


if __name__ == "__main__":
    # unpickle_data()
    pickle_data()
    check_pending_messages()
    # bot.auto_register()
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
