''' This file houses the global variables which store data in the database.
To communicate with the variable, from main.data import [variable] in your file.

Pylint disable justifications:
invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=invalid-name

import pickle
import os.path


def unpickle_data(file_name):
    '''
    Given a filename (without the .p extension), returns the value of the unpickled file.
    '''
    if not os.path.exists(f"{file_name}.p"):
        print(
            f"Warning: {file_name}.p not found. Data for that variable reset.", flush=True)
        return None
    try:
        data = pickle.load(open(f"{file_name}.p", "rb"))
    except:
        print(
            f"Warning: error loading {file_name}.p. Data for that variable reset.", flush=True)
        return None
    if not isinstance(data, list) and not isinstance(data, dict):
        print(f"Warning: error loading {file_name}.p. Data for that variable reset.", flush=True)
        return None

    print(f"Succesfully loaded {file_name}.p.", flush=True)
    return data


'''
## MESSAGES ##
The messages sub dictionary is composed like this example:
message_data = [
            {
                'message_id': <integer>
                'message': <string>
                'sending_u_id': <integer>,
                'timestamp': <datetime>
                'channel_id': <integer>
                'reacting_u_ids': [
                    <integers>
                ]
                'pinned': <boolean>
            }
        ]
The message_id is sequential from the old (0) to new (n-1).
'''  # pylint: disable=pointless-string-statement
temp = unpickle_data("message_data")
if temp == None:
    message_data = []
else:
    message_data = temp


'''
The pending_message_data list is identical to the message_data list, except it stores messages
that have a timestamp in the future.
These messages will be moved to message_data when the 'timestamp' is in the past.
'temporary_message_id' is only used for this list and will be updated when moved to message_data.
pending_message_data = [
            {
                'temporary_message_id': <integer>
                'message': <string>
                'sending_u_id': <integer>,
                'timestamp': <datetime>
                'channel_id': <integer>
                'reacting_u_ids': [
                    <integers>
                ]
                'pinned': <boolean>
            }
        ]
'''
temp = unpickle_data("pending_message_data")
if temp == None:
    pending_message_data = []
else:
    pending_message_data = temp
'''
### USER ###
The user sub dictionary is composed like this example:
user_data = [
            {
                'u_id': <integer>,
                'email': <string>,
                'first_name': <string>,
                'last_name': <string>,
                'handle': <string>
                'email': <stirng>
                'password': <string>,
                'is_owner_of_slackr': <boolean>,
                'is_logged_in': <boolean>
                'reset_code': <integer>
                'profile_img_url': <string>
            }
        ]
NOTE that user data will always contain the bot's data.
'''
temp = unpickle_data("user_data")
if temp == None:
    user_data = []
else:
    user_data = temp


'''
### CHANNEL ###
The all_channels sub dictionary is composed like this example:
[
    {
        "name": "REAL_NEWS_AT_FOX_NEWS",
        "channel_id": 99,
        "owner_members": [42013376969],
        "all_members": [42013376969, 80808080]
        "is_public": True
    }
]
We should only store the u_ids as we can just look up the names of the members with other functions.
'''
temp = unpickle_data("all_channels")
if temp == None:
    all_channels = []
else:
    all_channels = temp

'''
### STANDUP ###
Stores data rquired for standup.
Example:
[
    {
        'message': 'Hayden:i'm cool \n Rob: I'm cooler'
        'channel_id': channel_id,
        'u_id': u_id,
        "time_start": 01:11:50
        "time_finish": 01:16:50
    }
]

'''
temp = unpickle_data("standup_list")
if temp == None:
    standup_list = []
else:
    standup_list = temp

'''
## HANGMAN SESSIONS ##

List of dicts containing a channel ID and the word to be guessed.
#NOTE: only 1 hangman session can be active in a channel at a time.
Thus you must check whether a session is already active.

For instance:
[
    {
        'channel_id': 99,
        'word': "FromNowOnItWillOnlyBeAmericaFirstAmericaFirst"
        'guesses' = ['F', 'r']
    }
]
'''
temp = unpickle_data("hangman_sessions")
if temp == None:
    hangman_sessions = []
else:
    hangman_sessions = temp

'''
### NEXT_ID ###
Stores the next ID to be assigned for each of the data structures above.
Also stores the next image name.
{
    'message_id': <integer>,
    'u_id': <integer>,
    'channel_id': <integer>
    'image_name': <integer>
}
'''
temp = unpickle_data("next_id")
if temp == None:
    next_id = {}
else:
    next_id = temp
