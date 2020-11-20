'''
This module only tests for message/edit.
Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from msg_edit_test.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
unused-variable:
    If you observe below, messages are assigned 'msg1_3' for example for ease of comprehension, but
    are not necessarily used. If we were not not assigned these messages to such variables, it
    would make the code more confusing.
'''
# pylint: disable=unused-variable
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import requests
import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import URL_RESET, URL_MESSAGES, URL_CREATE, \
    URL_MSG_EDIT, URL_MSG_SEND


def test_basic():
    '''
    This is a sanity test for correct output based on all-correct input.
    Input = Correct token, u_id and permission_id
    Expected Output = {} with no errors.
    '''
    # debug mode
    # pdb.set_trace()

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create 2 channels
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "FOX_NEWS", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']

    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]

    # send 3 messages to each channel + 1 extra into channel2
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, \
        "message": "a"}).json()['message_id']
    msg2_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, \
        "message": "b"}).json()['message_id']
    msg3_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, \
        "message": "c"}).json()['message_id']
    msg1_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, \
        "message": "d"}).json()['message_id']
    msg2_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, \
        "message": "e"}).json()['message_id']
    msg3_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, \
        "message": "f"}).json()['message_id']

    # edit some messages
    requests.put(URL_MSG_EDIT, json={"token": token_0, "message_id": msg1_1, "message": \
        "new_msg_1(1)"})
    requests.put(URL_MSG_EDIT, json={"token": token_0, "message_id": msg2_1, "message": \
        "new_msg_2(1)"})
    requests.put(URL_MSG_EDIT, json={"token": token_1, "message_id": msg1_2, "message": \
        "new_msg_1(2)"})

    # retrieve messages
    payload = requests.get(
        URL_MESSAGES + f"?token={token_0}&channel_id={ch_id}&start=0").json()
    payload2 = requests.get(
        URL_MESSAGES + f"?token={token_1}&channel_id={ch_id2}&start=0").json()


    # confirm output.
    assert payload["start"] == 0 and payload["end"] == -1
    assert payload["messages"][2]["message"] == "new_msg_1(1)"
    assert payload["messages"][1]["message"] == "new_msg_2(1)"
    assert payload["messages"][0]["message"] == "c"

    assert payload2["start"] == 0 and payload2["end"] == -1
    assert payload2["messages"][2]["message"] == "new_msg_1(2)"
    assert payload2["messages"][1]["message"] == "e"
    assert payload2["messages"][0]["message"] == "f"


def test_invalid_token():
    '''
    Tests where the provided token is an invalid string.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token_0 = users_data[0]["token"]

    # send message to channel
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "a"}).json()['message_id']



    response = requests.put(URL_MSG_EDIT, json={"token": "NOT_VALID_TOKEN", "message_id": msg1_1, \
        "message": "new_msg_1(1)"})
    assert response.status_code == 400

def test_invalid_message_id():
    '''
    Tests where the provided message id is an invalid string
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token_0 = users_data[0]["token"]

    # send message to channel
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "a"}).json()['message_id']


    response = requests.put(URL_MSG_EDIT, json={"token": token_0, "message_id": "NOT_VALID_ID", \
        "message": "new_msg_1(1)"})
    assert response.status_code == 400 or response.status_code == 500

def test_user_not_authorised():
    '''
    Tests that edit is denied when user is not the author.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]

    # send message to channel
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "a"}).json()['message_id']

    response = requests.put(URL_MSG_EDIT, json={"token": token_1, "message_id": msg1_1, "message": \
        "new_msg_1(1)"})
    assert response.status_code == 400
