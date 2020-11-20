
'''
This module stores all the backend functions for the '/channel' route.
Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from channel.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''

# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name
import flask
from main.error import AccessError, InputError
from main.data import all_channels, user_data, message_data
import aux_.common as common
import aux_.discrete as discrete
import app.user as user  # for user details

###############
# FUNCTIONS
##############


def inv(token, channel_id, u_id):
    '''
    Requirements: correct token, ch_id and u_id.

    Search all_channels for the channel_id, then search up user details with u_id.
    Add the user details to all_channels.

    #Raises 2 possible InputErrors, 1 AccessError
    '''
    # assuming an invalid user will raise an InputError in user profile call.
    user.profile(token, u_id)

    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(description='Channel does not exist.')

    if common.user_in_channel(u_id, channel_id):
        raise InputError(description='User already in this channel.')
    # user is not authorized -> AccessError
    authorized_caller = common.decode_token(token)
    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            description='You do not have permission to invite to this channel.')

    # add to database
    all_channels[index]["all_members"].append(u_id)
    # if user is owner of slackr, they have owner privleges too
    if common.user_is_owner_of_slackr(u_id):
        all_channels[index]["owner_members"].append(u_id)
    return {}


def det(token, channel_id):
    '''
    Requirements: correct token and channel_id.

    Looks up all_channels for the ch_id and returns a dict containing the channel name, owner
    members and all members. Note: Will have to chop off the ch_id in the result.

    #Raises 1 possible InputError, 1 AccessError
    '''
    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(description='Channel does not exist.')

    # check if token is valid
    authorized_caller = common.decode_token(token)
    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            description='You do not have permission to view this channel.')

    details = {
        'name': all_channels[index]['name'],
        'owner_members': [],
        'all_members': []
    }
    for u_id in all_channels[index]['owner_members']:
        u_index = discrete.find_user(u_id)
        if u_index == -1:
            raise InputError(description="An unexpected error occured")
        member_dict = {
            'u_id': user_data[u_index]['u_id'],
            'name_first': user_data[u_index]['first_name'],
            'name_last': user_data[u_index]['last_name'],
            'profile_img_url': user_data[u_index]['profile_img_url']
        }
        details['owner_members'].append(member_dict)
    for u_id in all_channels[index]['all_members']:
        u_index = discrete.find_user(u_id)
        if u_index == -1:
            raise InputError(description="An unexpected error occured")
        member_dict = {
            'u_id': user_data[u_index]['u_id'],
            'name_first': user_data[u_index]['first_name'],
            'name_last': user_data[u_index]['last_name'],
            'profile_img_url': user_data[u_index]['profile_img_url']
        }
        details['all_members'].append(member_dict)
    return details


def msg(token, channel_id, start):
    '''
    Requirements: correct token and channel_id with start <= total  messages in the channel.

    Looks up message_data for messages with the same channel_id and returns up to 50 messages.
    It ranges from the most recent message to the 50th message, exclusive.

    #Raises 2 possible InputErrors, 1 AccessError
    '''
    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(description='Channel does not exist.')

    # check if token is valid.
    authorized_caller = common.decode_token(token)

    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            description='You do not have permission to view this channel.')

    # check if start > length of messages in the channel
    count = 0
    for message in message_data:
        if message["channel_id"] == channel_id:
            count += 1

    if start > count:
        raise InputError(description=f'You cannot retrieve messages from {start}')

    package = discrete.ch_msgs_retrieve(
        channel_id, start, authorized_caller['u_id'])
    # package is a dictionary containing a dictionary of messages and the start and end.
    if package == {}:
        raise InputError(
            description=f'Channel does not have messages beyond {start} point.')

    return package


def lev(token, channel_id):
    '''
    Requirements: correct token and channel_id.

    Looks up channel list and removes user from the channel.

    #Raises 1 possible InputError, 1 AccessError
    '''
    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(description='Channel does not exist.')

    # check if token is valid
    authorized_caller = common.decode_token(token)

    # if token is invalid or user with token not in the channel
    if authorized_caller == {"u_id": "error_invalid_token"}:
        raise AccessError(description='Invalid token.')
    if not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            description='Cannot leave a channel you have not joined.')
    # if user is also an owner, remove user as an owner first.
    # NOTE: cannot call remove_owner or it might raise an InputError if user is not an owner.
    common.remove_user(index, "owner_members", authorized_caller["u_id"])

    # remove the user dict from the all_members list
    common.remove_user(index, "all_members", authorized_caller["u_id"])

    return {}


def joi(token, channel_id):
    '''
    Requirements: correct token and channel_id.

    Looks up channel list and add user with token to the channel.

    #Raises 1 possible InputError, 1 AccessError
    '''
    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(description='Channel does not exist.')

    # check if token is valid
    authorized_caller = common.decode_token(token)

    # invalid token or user already in channel
    if authorized_caller == {"u_id": "error_invalid_token"}:
        raise AccessError(description='Invalid token.')
    if common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            description='Cannot join a channel if you already joined this channel.')

    # check if channel is private
    for channel_ in all_channels:
        if channel_id == channel_["channel_id"]:
            if not channel_["is_public"]:
                raise AccessError('You cannot join a private channel.')


    # add user to all_members
    all_channels[index]["all_members"].append(authorized_caller["u_id"])
    # if user is owner of slackr, they have owner privleges too
    if common.user_is_owner_of_slackr(authorized_caller['u_id']):
        all_channels[index]["owner_members"].append(authorized_caller["u_id"])
    return {}


def add_owner(token, channel_id, u_id):
    '''
    Requirements: correct token, channel_id and u_id.

    Retreives user details and add user as an owner of the channel

    #Raises 2 possible InputErrors, 1 AccessError
    '''

    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(description='Channel does not exist.')

    # check if token is valid
    authorized_caller = common.decode_token(token)['u_id']

    # invalid token or user is authorized.
    if authorized_caller == "error_invalid_token" or \
        (not common.user_is_owner_channel(authorized_caller, channel_id) and
         not common.user_is_owner_of_slackr(authorized_caller)):
        raise AccessError(
            description='You do not have permissions to add owners to this channel.')

    # check if user exists in the channel
    if not common.user_in_channel(u_id, channel_id):
        raise InputError(description='User is not in the channel')

    # check if user is owner
    if common.user_is_owner_channel(u_id, channel_id):
        raise InputError(description='User is already an owner')

    # add user to owner_members
    all_channels[index]["owner_members"].append(u_id)

    return {}


def rem_owner(token, channel_id, u_id):
    '''
    Requirements: correct token, channel_id and u_id.

    Retreives user details and remove user as an owner of the channel

    #Raises 2 possible InputErrors, 1 AccessError
    '''

    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(description='Channel does not exist.')

    # check if token is valid
    authorized_caller = common.decode_token(token)['u_id']

    # invalid token or user is authorized.
    if authorized_caller == "error_invalid_token" or \
        (not common.user_is_owner_channel(authorized_caller, channel_id) and
         not common.user_is_owner_of_slackr(authorized_caller)):
        raise AccessError(
            description='You do not have permissions to remove owners from this channel.')

    if common.user_is_owner_of_slackr(u_id):
        raise InputError(description="The owner of the slackr always has owner privleges - \
            cannot remove as owner.")

    # check if user exists in the channel
    if not common.user_in_channel(u_id, channel_id):
        raise InputError(description='User is not in the channel')

    # check if user is owner
    if not common.user_is_owner_channel(u_id, channel_id):
        raise InputError(description='User is not an owner')

    # remove user from owner_members
    if not common.remove_user(index, "owner_members", u_id):
        raise InputError(description='User is not an owner.')

    return {}
