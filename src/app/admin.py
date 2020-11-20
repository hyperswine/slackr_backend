'''
This module stores all the backend functions for the '/admin' route.
Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from admin.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import app.user as user
from main.error import AccessError, InputError
import aux_.discrete as discrete
import aux_.common as common
import main.data as data


def change_permissions(token, u_id, permission_id):
    '''
    Requirements: correct token, u_id and permission_id

    Given an admin's token, changes a user's global permissions to reflect a given permission_id.
    This can be simply demoting a user from owner_member to member.
    An admin can demote himself, other admins and standard users.

    Output - {}

    # Possible: 2 InputErrors, 1 AccessError
    '''

    # Assuming user_profile() raises InputError if invalid user.
    user.profile(token, u_id)

    # invalid permission ID -> InputError
    if permission_id not in (1, 2):
        raise InputError('Invalid permission type.')

    # user is not authorized -> AccessError
    authorized_caller = common.decode_token(token)
    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_is_owner_of_slackr(authorized_caller["u_id"]):
        raise AccessError(
            "You do not have permission to make changes to users' permissions.")

    # modify a user's global permissions.
    if not discrete.modify_global_permissions(u_id, permission_id):
        raise InputError('User is not in the slackr.')

    return {}


def remove_user(token, u_id):
    '''
    Requirements: correct token and u_id.

    As an admin, remove a given user from the slackr completely.
    The user will be removed from all channels and user_data, but their messages
    will still be there. NOTE: can also make the user as [deleted] next
    to their messages.

    Output - {}

    # Possible: 1 InputError, 1 AccessError
    '''
    # Assuming user_profile() raises InputError if invalid user.
    user.profile(token, u_id)

    # user is not authorized -> AccessError
    authorized_caller = common.decode_token(token)
    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_is_owner_of_slackr(authorized_caller["u_id"]):
        raise AccessError(
            "You do not have permission to remove users.")

    # remove user from all channels
    for channel in data.all_channels:
        common.remove_user(channel["channel_id"], "owner_members", u_id)
        common.remove_user(channel["channel_id"], "all_members", u_id)

    # remove all the user's messages
    for message in data.message_data[:]:
        print("checking msg", flush=True)
        if message['sending_u_id'] == u_id:
            data.message_data.remove(message)
            print("message removed", flush=True)

    # remove pending messages
    for pending_msg in data.pending_message_data[:]:
        if pending_msg['sending_u_id'] == u_id:
            data.pending_message_data.remove(pending_msg)

    # in all msgs, remove their react from it
    for message in data.message_data:
        if u_id in message['reacting_u_ids']:
            message['reacting_u_ids'].remove(u_id)

    # remove user from user_data
    for userX in data.user_data:
        if userX["u_id"] == u_id:
            data.user_data.remove(userX)
            break

    return {}
