'''
Core message functions.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from channels.py, but we run the server from server.py, there will be \
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import aux_.common as aux_common
from main.data import all_channels, next_id
from main.error import InputError, AccessError

def list_(token):
    '''
    ## DESCRIPTION ##
    Given a token, returns the channels the user is in.

    ## TYPES ##
    token - string

    ## RETURN VALUE ##
    {'channels': [
        {
            'channel_id': <integer>,
            'name': string
        },
        ...
    ]}

    ## EXCEPTIONS ##
    AccessError if:
        - Token is invalid
    '''
    global all_channels
    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")

    channels_dict = {'channels': []}
    for channel in all_channels:
        if aux_common.user_in_channel(user['u_id'], channel['channel_id']):
            channels_dict['channels'].append({
                'channel_id': channel['channel_id'],
                'name': channel['name']
            })

    return channels_dict

def listall(token):
    '''
    ## DESCRIPTION ##
    Given a token, returns all channels (except private ones)

    ## TYPES ##
    token - string

    ## RETURN VALUE ##
    {'channels': [
        {
            'channel_id': <integer>,
            'name': string
        },
        ...
    ]}

    ## EXCEPTIONS ##
    AccessError if:
        - Token is invalid
    '''
    global all_channels
    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")

    channels_dict = {'channels': []}
    for channel in all_channels:
        if channel['is_public']:
            channels_dict['channels'].append({
                'channel_id': channel['channel_id'],
                'name': channel['name']
            })

    return channels_dict

def create(token, name, is_public):
    '''
    ## DESCRIPTION ##
    Given a token, name, and is_public boolean, creates a new channel with the properties passed.

    ## TYPES ##
    token - string
    name - string
    is_public - boolean

    ## RETURN VALUE ##
    { channel_id }

    ## EXCEPTIONS ##
    AccessError if:
        - Token is invalid
    InputError if:
        - The name is < 1 or > 20 characters long
    '''
    global all_channels, next_id
    user = aux_common.decode_token(token)
    if user['u_id'] == 'error_invalid_token' or not isinstance(user['u_id'], int):
        raise AccessError(description="Invalid token")
    if len(name) < 1 or len(name) > 20:
        raise InputError(description="Name of channel must be 1 to 20 characters long.")

    next_ch_id = next_id.get('channel_id')
    if not next_ch_id:  # key does not exist yet
        next_id['channel_id'] = 0
        next_ch_id = 0
    next_id['channel_id'] += 1

    new_channel_dict = {
        "name": name,
        "channel_id": next_ch_id,
        "owner_members": [user['u_id']],
        "all_members": [user['u_id']],
        "is_public": is_public
    }
    all_channels.append(new_channel_dict)
    return {'channel_id': next_ch_id}
