'''
Core message functions.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from message.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import threading
from datetime import datetime
import aux_.common as aux_common
import aux_.discrete as aux_discrete
from main.data import message_data, pending_message_data, next_id
from main.error import AccessError, InputError

def send(token, channel_id, message):
    '''
    ## DESCRIPTION ##
    Given a token, channel_id, and message, decodes the token, and adds the
    message 'message' into the messages database with the user of the token.

    ## TYPES ##
    token - string
    channel_id - integer
    message - string

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - Message is more than 1000 characters
        - Message is 0 characters.
    AccessError
        - Token is invalid
        - The user has not joined the channel they are trying to post to
    '''
    global message_data, next_id
    if len(message) <= 0 or len(message) > 1000:
        raise InputError(
            description="Message must be between 1 and 1000 characters long.")

    user = aux_common.decode_token(token)

    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description='Invalid token')

    if not aux_common.user_in_channel(user['u_id'], channel_id):
        raise AccessError(
            description='User is not in the channel that message is being sent to')

    next_msg_id = next_id.get('message_id')
    if not next_msg_id:  # key does not exist yet
        next_id['message_id'] = 0
        next_msg_id = 0

    next_id['message_id'] += 1

    message_dict = {
        'message_id': next_msg_id,
        'message': message,
        'sending_u_id': user['u_id'],
        'timestamp': datetime.utcnow(),
        'channel_id': int(channel_id),
        'reacting_u_ids': [],
        'pinned': False
    }

    message_data.append(message_dict)
    return {'message_id': len(message_data) - 1}


def send_later(token, channel_id, message, time_to_send):
    '''
    ## DESCRIPTION ##
    Given a token, channel_id, and message, decodes the token, and adds 'message' into the pending
    messages database with the requested time_to_send
    instead of datetime.utcnow()

    ## TYPES ##
    token - string
    channel_id - integer
    message - string
    time_to_send - datetime

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - Message is more than 1000 characters
        - Message is 0 characters.
        - The time_to_send is in the past.
    AccessError if
        - Token is invalid
        - The user has not joined the channel they are trying to post to
    '''
    global pending_message_data
    if len(message) <= 0 or len(message) > 1000:
        raise InputError(
            description='Message must be between 1 and 1000 characters long.')
    if time_to_send < datetime.utcnow():
        raise InputError(description='The date to send must be in the future.')

    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int) or \
            not aux_common.user_in_channel(user['u_id'], channel_id):
        raise AccessError(
            description='User is not in the channel that message is being sent to')

    message_dict = {
        'temporary_message_id': len(pending_message_data),
        'message': message,
        'sending_u_id': user['u_id'],
        'timestamp': time_to_send,
        'channel_id': int(channel_id),
        'reacting_u_ids': [],
        'pinned': False
    }
    print(time_to_send, flush=True)
    pending_message_data.append(message_dict)

    return {'message_id': (len(message_data) - 1)}


def check_pending_messages():
    '''
    ## DESCRIPTION ##
    Every 2 seconds, checks if any messages in pending_message_data has a timestamp in the past.
    If so, assigns message_id and moves it to message_data
    '''
    global message_data, pending_message_data
    threading.Timer(2.0, check_pending_messages).start()
    if len(pending_message_data) == 0:
        return
    for item in pending_message_data:
        if item['timestamp'] < datetime.utcnow():
            next_msg_id = next_id.get('message_id')
            if not next_msg_id:  # key does not exist yet
                next_id['message_id'] = 0
                next_msg_id = 0

            next_id['message_id'] += 1
            print("moving message")
            message_dict = {
                'message_id': next_msg_id,
                'message': item['message'],
                'sending_u_id': item['sending_u_id'],
                'timestamp': item['timestamp'],
                'channel_id': item['channel_id'],
                'reacting_u_ids': item['reacting_u_ids'],
                'pinned': item['pinned']
            }

            message_data.append(message_dict)
            pending_message_data.remove(item)


def react(token, message_id, react_id):
    '''
    ## DESCRIPTION ##
    Given a token, message_id, and react_id, adds the 'token' user to the 'reacting_u_ids' list
    of the corresponding 'message_id'.

    ## TYPES ##
    token - string
    message_id - integer
    react_id - integer

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - react_id is not 1
        - message_id is not a valid message within a channel the authorised user has joined
        - User has already 'reacted' to this message.

    AccessError if
        - Token is invalid
    '''
    global message_data
    message_index = aux_discrete.find_message(message_id)
    if message_index == -1:
        raise InputError(description='Message ID is invalid.')

    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")

    if not aux_common.user_in_channel(user['u_id'], message_data[message_index]['channel_id']):
        raise InputError(
            description="User is not in the channel that the message to react to is in.")

    if react_id != 1:
        raise InputError(description="Invalid react ID")

    if user['u_id'] in message_data[message_index]['reacting_u_ids']:
        raise InputError(description="Message already reacted to")

    message_data[message_index]['reacting_u_ids'].append(user['u_id'])
    return {}


def unreact(token, message_id, react_id):
    '''
    ## DESCRIPTION ##
    Given a token, message_id, and react_id, removes the 'token' user from the 'reacting_u_ids' list
    of the corresponding 'message_id'.

    ## TYPES ##
    token - string
    message_id - integer

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - react_id is not 1
        - message_id is not a valid message within a channel the authorised user has joined
        - User has not reacted to this message

    AccessError if
        - Token is invalid
    '''
    global message_data
    message_index = aux_discrete.find_message(message_id)
    if message_index == -1:
        raise InputError(description='Message ID is invalid.')

    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")

    if not aux_common.user_in_channel(user['u_id'], message_data[message_index]['channel_id']):
        raise InputError(
            description="User is not in the channel that the message to unreact to is in.")

    if react_id != 1:
        raise InputError(description="Invalid react ID")

    if user['u_id'] not in message_data[message_index]['reacting_u_ids']:
        raise InputError(description="Message not reacted to")

    message_data[message_index]['reacting_u_ids'].remove(user['u_id'])
    return {}


def pin(token, message_id):
    '''
    ## DESCRIPTION ##
    Given a token and message_id, changes the 'pinned' attribute of the corresponding 'message_id'
    dictinoary to True.

    ## TYPES ##
    token - string
    message_id - integer

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - message_id is invalid
        - the user is not an owner
        - message is already pinned

    AccessError if
        - The user is not a member of the channel that the message is within
        - Token is invalid
    '''
    global message_data
    message_index = aux_discrete.find_message(message_id)
    if message_index == -1:
        raise InputError(description='Message ID is invalid.')

    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")

    if not aux_common.user_in_channel(user['u_id'], message_data[message_index]['channel_id']):
        raise InputError(
            description="User is not in the channel that the message to pin to is in.")

    if message_data[message_index]['pinned']:
        raise InputError(description="Message already pinned")

    if not aux_common.user_is_owner_of_slackr(user['u_id']) and not \
            aux_common.user_is_owner_channel(user['u_id'], message_data[message_index]['channel_id']):
        raise InputError(
            description="User is not owner of the slackr and not owner of the channel")

    message_data[message_index]['pinned'] = True

    return {}


def unpin(token, message_id):
    '''
    ## DESCRIPTION ##
    Given a token and message_id, changes the 'pinned' attribute of the corresponding 'message_id'
    dictinoary to False.

    ## TYPES ##
    token - string
    message_id - integer

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - message_id is invalid
        - the user is not an owner
        - message is not pinned

    AccessError if
        - The user is not a member of the channel that the message is within
        - Token is invalid
    '''
    global message_data
    message_index = aux_discrete.find_message(message_id)
    if message_index == -1:
        raise InputError(description='Message ID is invalid.')

    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")

    if not aux_common.user_in_channel(user['u_id'], message_data[message_index]['channel_id']):
        raise InputError(
            description="User is not in the channel that the message to unpin to is in.")

    if not message_data[message_index]['pinned']:
        raise InputError(description="Message not yet pinned")

    if not aux_common.user_is_owner_of_slackr(user['u_id']) and not \
            aux_common.user_is_owner_channel(user['u_id'], message_data[message_index]['channel_id']):
        raise InputError(
            description="User is not owner of the slackr and not owner of the channel")

    message_data[message_index]['pinned'] = False

    return {}


def remove(token, message_id):
    '''
    ## DESCRIPTION ##
    Given a token and message_id, if the user has requisite permissions, removes the message
    message_id

    ## TYPES ##
    token - string
    message_id - integer

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - message_id is invalid

    AccessError if:
        - Token is invalid

    AccessError if ALL OF THE FOLLOWING:
        - User is not the authorised user (the creator of message)
        - User is not an owner of this channel
        - User is not an owner of the slackr
    '''
    global message_data
    msg_index = aux_discrete.find_message(message_id)
    if msg_index == -1:
        raise InputError(description='Message ID is invalid.')

    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")

    if not aux_common.user_is_owner_channel(user['u_id'], message_data[msg_index]['channel_id']) \
            and not aux_common.user_is_owner_of_slackr(user['u_id']) and \
            message_data[msg_index]['sending_u_id'] != user['u_id']:
        raise AccessError(
            description="User does not have requisite permission to remove the message")

    message_data.pop(msg_index)
    return {}


def edit(token, message_id, message):
    '''
    ## DESCRIPTION ##
    Given a token and message_id, if the user has requisite permissions, changes the message to
    the new message.

    ## TYPES ##
    token - string
    message_id - integer
    message - string

    ## RETURN VALUE ##
    {}

    ## EXCEPTIONS ##
    InputError if
        - message_id is invalid
        - new message is empty or greater than 1000 characters

    AccessError if:
        - Token is invalid

    AccessError if ALL OF THE FOLLOWING:
        - User is not the authorised user (the creator of message)
        - User is not an owner of this channel
        - User is not an owner of the slackr
    '''
    global message_data
    if len(message) <= 0 or len(message) > 1000:
        raise InputError(
            description="Message must be between 0 and 1000 characters long")

    msg_index = aux_discrete.find_message(message_id)
    if msg_index == -1:
        raise InputError(description='Message ID is invalid.')

    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")
    if not aux_common.user_is_owner_channel(user['u_id'], message_data[msg_index]['channel_id']) \
            and not aux_common.user_is_owner_of_slackr(user['u_id']) \
            and message_data[msg_index]['sending_u_id'] != user['u_id']:
        raise AccessError(
            description="User does not have requisite permission to remove the message")

    message_data[msg_index]['message'] = message
    return {}
