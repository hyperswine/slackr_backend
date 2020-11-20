'''
Functions which perform pickling for data persistence.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from pickle.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import threading
import pickle
from main.data import pending_message_data, message_data, user_data, all_channels, standup_list, next_id, hangman_sessions


def pickle_data():
    '''
    Pickles the data every 1 second as follows:
    message_data => message_data.p
    user_data => user_data.p
    all_channels => all_channels.p
    etc.
    '''
    global message_data, pending_message_data, user_data, all_channels, standup_list, next_id
    threading.Timer(1.0, pickle_data).start()
    # print("pickling...")
    with open('message_data.p', 'wb') as message_file:
        pickle.dump(message_data, message_file)
    with open('pending_message_data.p', 'wb') as pending_message_file:
        pickle.dump(pending_message_data, pending_message_file)
    with open('user_data.p', 'wb') as user_file:
        pickle.dump(user_data, user_file)
    with open('all_channels.p', 'wb') as channels_file:
        pickle.dump(all_channels, channels_file)
    with open('standup_list.p', 'wb') as standup_file:
        pickle.dump(standup_list, standup_file)
    with open('next_id.p', 'wb') as next_id_file:
        pickle.dump(next_id, next_id_file)
    with open('hangman_sessions.p', 'wb') as hangman_sessions_file:
        pickle.dump(hangman_sessions, hangman_sessions_file)
