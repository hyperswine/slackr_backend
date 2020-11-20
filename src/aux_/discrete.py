'''
DISCRETE auxiliary functions to be used discretely by individual core files.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from discrete.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import re
import datetime
import main.data as data
import app.message as message


def ch_msgs_retrieve(channel_id, start, u_id):
    '''
    Loop through message data and return a package containing all the messages with the
    channel_id starting from index 'start'.
    The authorised user is u_id
    '''
    package = {"messages": [], "start": start, "end": 0}
    index = len(data.message_data) - start - 1
    count = 0
    while index != -1 and count < start + 50:
        if data.message_data[index]['channel_id'] == channel_id:
            message_dict = {
                'message_id': data.message_data[index]['message_id'],
                'u_id': data.message_data[index]['sending_u_id'],
                'message': data.message_data[index]['message'],
                'time_created': int(data.message_data[index]['timestamp'].\
                    replace(tzinfo=datetime.timezone.utc).timestamp()),
                'reacts': [{'react_id': 1,
                            'u_ids': data.message_data[index]['reacting_u_ids'],
                            'is_this_user_reacted': \
                            bool(u_id in data.message_data[index]['reacting_u_ids'])}],
                'is_pinned': data.message_data[index]['pinned']
            }
            package['messages'].append(message_dict)
            count += 1
        index -= 1
    if index == -1:
        package['end'] = -1
    else:
        package['end'] = start + 50
    return package


def standup_data(time_start, time_finish, channel_id, u_id):
    '''
    Appends a channel standup to the standup queue.
    '''
    data.standup_list.append(
        {
            'message': '',
            'channel_id': channel_id,
            'u_id': u_id,
            'time_start': time_start,
            'time_finish': time_finish  # in case standup finishes early.
        }
    )


def find_standup(channel_id):
    '''
    Searches standup_list for the standup with channel_id returns its index.
    Returns -1 if not found.
    '''
    index = 0
    for standup in data.standup_list:
        if standup["channel_id"] == channel_id:
            return index
        index += 1
    return -1


def send_standup(token, channel_id, standup_index):
    '''
    Uses message_send to send the standup message with standup_index
    '''
    if data.standup_list[standup_index]['message'] == "":
        data.standup_list[standup_index][
            'message'] = "No one sent a message during the standup :("
    else:
        data.standup_list[standup_index]['message'].lstrip()
    message.send(token, channel_id,
                 data.standup_list[standup_index]['message'])

#### MESSAGE DATA FUNCTIONS ###


def find_message(message_id):
    '''
    ## DESCRIPTION ##
    Given a message_id, tries to find a message with that ID in message_data and returns the index
    to the corresponding message dictionary

    ## TYPES ##
    message_id - integer

    ## RETURN VALUE ##
    If message_id is found, the index
    If message_id is not found, -1
    '''
    index = 0
    for curr_message in data.message_data:
        if curr_message['message_id'] == message_id:
            return index
        index += 1
    return -1

### USER DATA FUNCTIONS ###

def find_uid(email):
    '''
    Given an email, return the u_id of that guy.
    '''
    index = 0
    for user in data.user_data:
        if user['email'] == email:
            return index
        index += 1
    return -1

def find_user(u_id):
    '''
    ## DESCRIPTION ##
    Given a u_id, tries to find a user with that ID in user_data and returns the index to
    the corresponding message dictionary

    ## TYPES ##
    message_id - integer

    ## RETURN VALUE ##
    If message_id is found, the index
    If message_id is not found, -1
    '''
    index = 0
    for user in data.user_data:
        if user['u_id'] == u_id:
            return index
        index += 1
    return -1


def modify_global_permissions(u_id, permission_id):
    '''
    Modify a user's global permissions. NOTE we could probably merge this with the one above later
    on.
    '''
    for user in data.user_data:
        if user["u_id"] == u_id:
            user["is_owner_of_slackr"] = bool(permission_id == 1)
            return True

    return False

def check_email_valid(email):
    """
    Given code from spec
    source:https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    """
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  # pylint: disable = anomalous-backslash-in-string
    return bool(re.search(regex, email))

def check_email_in_use(email):
    """Checks through all emails to see if it is use. If it is, Returns False, and if
     it isnt returns TRUE"""
    for user in data.user_data:
        if user['email'] == email:
            return False
    return True


def check_handle_in_use(handle_str):
    """
    Checks users handle same logic as check_email in use. If handle is in use returns false,
    otherwise returns true.
    """
    for user in data.user_data:
        if user['handle_str'] == handle_str:
            return False
    return True

def user_exists(u_id):
    """Check if the user exists through their user id
        Returns True if u_id is valid, Returns False if not"""

    for user in data.user_data:
        if user['u_id'] == u_id:
            return True

    return False

### AUTH FUNCTIONS ###


def new_handle(first_name, last_name):
    '''
    Generates a new user handle based on concatenation of first name and last name.
    Returns the new handle string.
    If longer than 20 characters, cuts off the handle.
    If already used, cuts off last few chars and adds number.
    If passed values are not string, raises TypeError.
    '''
    if not isinstance(first_name, str) or not isinstance(last_name, str):
        raise TypeError
    handle = first_name + last_name
    if len(handle) > 20:
        handle = handle[:20]

    matching_existing_handles = 0
    for user in data.user_data:
        if user['handle'] == handle:
            matching_existing_handles += 1

    if matching_existing_handles == 0:
        return handle

    number_to_append = matching_existing_handles
    len_req_number = len(str(number_to_append))
    if len_req_number + len(handle) > 20:
        len_over_twenty_chars = len_req_number + len(handle) - 20
        handle = handle[:(19-len_over_twenty_chars)] + str(number_to_append)
        return handle

    handle = handle + str(number_to_append)
    return handle
