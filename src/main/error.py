'''
Provided file in spec.
Will disable any pylint errors that arise, since this file was provided.
'''
# pylint: disable=missing-class-docstring

from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'
