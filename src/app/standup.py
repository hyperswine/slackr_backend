'''
Core standup functions.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from standup.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import datetime
from threading import Timer
import aux_.common as common
import aux_.discrete as discrete
from main.error import InputError, AccessError
import main.data as data


def start(token, channel_id, length):
    '''
    Requirements: correct channel_id and token

    This will start a standup session for 'length' seconds. Messages sent to this session must be
    through 'send'.
    A message sent will be appended to the final message using send.
    At time = length, the message package will be sent over to message_data.

    #Raises 2 possible InputErrors
    '''
    # preliminary checks
    if common.ch_id_exists(channel_id) == -1:
        raise InputError('Invalid Channel. Cannot start standup.')

    if active(token, channel_id)['is_active']:
        raise InputError(
            'A standup is active. Only 1 standup may be running at a time.')

    authorized_caller = common.decode_token(token)
    if authorized_caller["u_id"] == {"u_id": "error_invalid_token"} or not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError('You do not have permission to do this.')

    # check if length is valid. Assuming that a standup lasts for at least 1 second.
    if length < 1:
        raise InputError(description='You cannot start a standup for a time less than 1 second.')

    # keep start and finish for better accuracy
    time_start = datetime.datetime.utcnow()

    time_finish = time_start + datetime.timedelta(seconds=length)

    discrete.standup_data(time_start, time_finish,
                          channel_id, authorized_caller['u_id'])

    index = discrete.find_standup(channel_id)
    # at length = length seconds, sends all the messages from the queue as a complete package
    Timer(length, discrete.send_standup, [token, channel_id, index]).start()
    Timer(length + 1, data.standup_list.pop, [index]).start()
    return {'time_finish': int(time_finish.replace(tzinfo=datetime.timezone.utc).timestamp())}


def active(token, channel_id):
    '''
    Requirements: correct channel_id.

    Checks whether a standup with channel_id exists in standup_list.
    It will simply retrieve from data.py and return it in a neat package.

    #Raises 1 possible InputError
    '''
    # check for valid token
    common.token_valid(token)

    # check for valid channel
    if common.ch_id_exists(channel_id) == -1:
        raise InputError('This channel does not exist.')

    is_active = False
    time_finish = None

    for channel in data.standup_list:
        if channel["channel_id"] == channel_id:
            is_active = True
            time_finish = int(channel["time_finish"].replace(
                tzinfo=datetime.timezone.utc).timestamp())

    return {'is_active': is_active, 'time_finish': time_finish}


def send(token, channel_id, message):
    '''
    Requirements: correct token, channel_id and len(message) <= 1000

    Appends a message to the standup_messages list. It will depend on an aux_ function buffering it
    first before appending at the end of the list.

    #Raises 3 Possible InputErrors, 1 Access Error
    '''

    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError('Channel does not exist.')

    # message > 1000 characters
    if len(message) > 1000 or len(message) == 0:
        raise InputError(
            description=f'Your message is {len(message)-1000} over the limit. Your message cannot be over 1000 \
                characters')

    # user is not authorized -> AccessError
    authorized_caller = common.decode_token(token)
    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            'You cannot send a standup message in this channel which you are not part of.')

    # active standup false -> InputError
    if not active(token, channel_id)['is_active']:
        raise InputError('Standup not active.')

    index = discrete.find_standup(channel_id)
    u_index = discrete.find_user(authorized_caller['u_id'])
    data.standup_list[index]['message'] += f"\n{data.user_data[u_index]['handle']}: {message}"
    print(f"message now {data.standup_list[index]['message']}", flush=True)
    return {}
