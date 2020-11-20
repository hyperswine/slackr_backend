'''
Workspace reset core function.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from workspace.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-0statement
# pylint: disable=invalid-name

from main.data import message_data, pending_message_data, user_data, all_channels, standup_list, next_id, hangman_sessions
import os

def workspace_reset():
    '''
    ## DESCRIPTION ##
    Resets the workspace to a fresh state.
    '''
    global message_data, pending_message_data, user_data, all_channels, standup_list, next_id, hangman_sessions
    message_data.clear()
    pending_message_data.clear()
    user_data.clear()
    all_channels.clear()
    standup_list.clear()
    next_id.clear()
    hangman_sessions.clear()

    # Remove all profile pics except default ones
    currdir = os.getcwd()
    for root, dirs, files in os.walk(currdir + "/profile_images"):

        for f in files:
            print(f, flush=True)
            if "default" not in f and "bot" not in f:
                print("here")
                os.remove(currdir + "/profile_images/" + f)
