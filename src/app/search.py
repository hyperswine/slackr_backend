'''
Core search functions.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from search.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import datetime
import aux_.common as aux_common
from main.data import message_data
from main.error import AccessError



def search(token, query_str):
    '''
    ## DESCRIPTION ##
    Given a query string, return a collection of messages in all of the channels
    that the user has joined that match the query. Results are sorted from most
    recent message to least recent message.

    ## TYPES ##
    token - string
    query_str - string

    ## RETURN VALUE ##
    {messages}

    ## EXCEPTIONS ##
    N/A
    '''

    message_list = []

    user_id = aux_common.decode_token(token)

    if user_id == {'u_id': "error_invalid_token"}:
        raise AccessError(description="Invalid Token")

    for message in message_data:
        if aux_common.user_in_channel(user_id['u_id'], message['channel_id']):
            if query_str in message['message']:
                message_dict = {
                    "message_id": message['message_id'],
                    "u_id": message['sending_u_id'],
                    "message": message['message'],
                    "time_created": message['timestamp'].replace(tzinfo=datetime.timezone.utc).\
                        timestamp(),
                    "reacts": [{'react_id': 1,
                                'u_ids': message['reacting_u_ids'],
                                'is_this_user_reacted': \
                                    bool(user_id['u_id'] in message['reacting_u_ids'])}],
                    "is_pinned": message['pinned'],
                }
                message_list.append(message_dict)

    #print(f"returning {'messages': message_dict}", flush=True)
    return{'messages': message_list}
