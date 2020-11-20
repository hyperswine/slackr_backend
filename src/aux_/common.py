'''
COMMON auxiliary functions to be used commonly by all core files.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from common.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import jwt
from main.data import all_channels, user_data
from main.error import AccessError
import aux_.discrete as discrete
SECRET_PASSKEY = "Pepega-G0Od_Mem3s-KEKW"


def Common(a, b):
    '''
    A lambda function that does almost half of the functionality that we require.

    Parameters
        a - the thing your searching for
        b - the haystack

    Returns the index of the thing you're searching for in the haystack.
    '''
    return lambda x: _expression, a, b


def _expression(A, B):
    '''
    Helper function for Common()
    '''
    for i, b in enumerate(B):
        if A == b[str(A)]:
            return i

    return False


def encode_token(u_id):
    '''
    Given a u_id dictionary of the form {"u_id": u_id}, generates a token with
    the secret passkey and returns it.
    '''
    return jwt.encode(u_id, SECRET_PASSKEY, algorithm='HS256').decode('utf-8')


def decode_token(token):
    '''
    Given a token, decodes to reveal a dictionary of the form {"u_id": u_id}
    An invalid token will decode to nonsense, or return {"u_id": "error_invalid_token"}
    If the user is not logged in, will also return {"u_id", "error_invalid_token"}
    '''
    try:
        decoded = jwt.decode(token.encode('utf-8'),
                             SECRET_PASSKEY, algorithms=['HS256'])
    except:  # pylint: disable=bare-except
        return {"u_id": "error_invalid_token"}

    user_dict = {}
    for user in user_data:
        if user['u_id'] == decoded['u_id']:
            user_dict = user
    if user_dict == {} or not user_dict['is_logged_in']:
        return {"u_id": "error_invalid_token"}
    return {"u_id": user_dict['u_id']}


def user_in_channel(u_id, channel_id):
    '''
    ## DESCRIPTION ##
    Given a u_id integer and channel_id integer, returns True if user is in that channel, and
    False if not.

    ## EXCEPTIONS ##
    If a u_id or channel_id cannot be found, returns False by default.
    '''
    ch_index = ch_id_exists(channel_id)
    if ch_index == -1:
        return False
    if u_id in all_channels[ch_index]['all_members']:
        return True
    return False


def user_is_owner_channel(u_id, channel_id):
    '''
    ## DESCRIPTION ##
    Given a u_id integer and channel_id integer, returns True if user is in that channel, and
    False if not.

    ## EXCEPTIONS ##
    If a u_id or channel_id cannot be found, returns False by default.
    '''
    ch_index = ch_id_exists(channel_id)
    if ch_index == -1:
        return False
    if u_id in all_channels[ch_index]['owner_members']:
        return True
    return False


def user_is_owner_of_slackr(u_id):
    '''
    Given a u_id integer, returns True if user owner of the slackr, and
    False if not.

    ## EXCEPTIONS ##
    If a u_id cannot be found, returns False by default.
    '''
    u_index = discrete.find_user(u_id)
    if u_index == -1:
        return False
    return user_data[u_index]['is_owner_of_slackr']


def ch_name_exists(name):
    '''
    Return boolean if channel name exists
    '''
    for channels in all_channels:
        if name == channels["names"]:
            return True

    return False


def ch_id_exists(channel_id):
    '''
    Return index if channel id exists
    If not, return -1
    '''
    index = 0
    for channels in all_channels:
        if channel_id == channels["channel_id"]:
            return index
        index += 1

    return -1


def remove_user(ch_index, list_string, u_id):
    '''
    Loop through the list of member dicts and remove the dict corresponding the the correct u_id.
    This can be used for both all_members and owner_members.
    '''
    global all_channels
    for member in all_channels[ch_index][list_string]:
        if member == u_id:
            all_channels[ch_index][list_string].remove(member)
            return True

    return False


def token_valid(token):
    '''
    Checks whether a token is valid. If not, raises AccessError.
    '''
    authorized_caller = decode_token(token)
    if authorized_caller["u_id"] == {"u_id": "error_invalid_token"} or decode_token(token) == {"u_id": "error_invalid_token"}:
        raise AccessError('You do not have permission to do this.')


if __name__ == '__main__':
    # Basic tests, to be removed when we are satisfied
    RESULT_TOKEN = encode_token({'u_id': 124154109851092852190})
    print(RESULT_TOKEN)
    print(decode_token(RESULT_TOKEN))
    # Tampered token
    print(decode_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoxMjQxNT\
        QxMDk4NTEwATI4NTIxOTB9.zC2HfIu4rD1cPnl65TbscO5PAhmVCCwA7eJjBf_uJYw"))
    # CHANGED HERE wOT to wAt
