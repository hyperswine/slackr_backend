'''
This module only tests for message/react.
Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from msg_edit_test.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
unused-variable and too-many-locals:
    If you observe below, messages are assigned 'msg1_3' for example for ease of comprehension, but
    are not necessarily used. If we were not not assigned these messages to such variables, it
    would make the code more confusing.
'''
# pylint: disable=unused-variable
# pylint: disable=too-many-locals
# pylint: disable=no-name-in-module
# pylint: disable=import-error

import requests
import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import URL_RESET, URL_MESSAGES, URL_CREATE,\
    URL_MSG_SEND, invite_user_channel, URL_INVITE, URL_MSG_REACT


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

    # ch_id: owner = token_0; member = token_0, token_2
    # ch_id2: owner = token1; member = token_1
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "FOX_NEWS", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']

    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]
    token_2 = users_data[2]["token"]
    invite_user_channel(token_0, ch_id, users_data[2]['u_id'], URL_INVITE)
    # send 3 messages to each channel + 1 extra into channel2
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "a"}).json()['message_id']
    msg2_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "b"}).json()['message_id']
    msg3_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "c"}).json()['message_id']
    msg1_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": \
        "d"}).json()['message_id']
    msg2_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": \
        "e"}).json()['message_id']
    msg3_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": \
        "f"}).json()['message_id']

    # react to some messages
    requests.post(URL_MSG_REACT, json={"token": token_0, "message_id": msg1_1, "react_id": 1})\
        .json()
    requests.post(URL_MSG_REACT, json={"token": token_2, "message_id": msg1_1, "react_id": 1})\
        .json()
    requests.post(URL_MSG_REACT, json={"token": token_2, "message_id": msg2_1, "react_id": 1})\
        .json()
    requests.post(URL_MSG_REACT, json={"token": token_1, "message_id": msg1_2, "react_id": 1})\
        .json()

    # retrieve messages
    payload = requests.get(
        URL_MESSAGES + f"?token={token_0}&channel_id={ch_id}&start=0").json()
    payload2 = requests.get(
        URL_MESSAGES + f"?token={token_1}&channel_id={ch_id2}&start=0").json()


    # confirm output.
    assert payload["messages"][2]["reacts"][0]['u_ids'] == [users_data[0]['u_id'], users_data[2]\
        ['u_id']]
    assert payload["messages"][1]["reacts"][0]['u_ids'] == [users_data[2]['u_id']]

    assert payload2["messages"][2]["reacts"][0]['u_ids'] == [users_data[1]['u_id']]


def test_already_reacted():
    '''Test error occurs where user already reacted'''
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

    requests.post(URL_MSG_REACT, json={"token": token_0, "message_id": msg1_1, \
        "react_id": 1}).json()

    response = requests.post(URL_MSG_REACT, json={"token": token_0, "message_id": msg1_1, \
        "react_id": 1})
    assert response.status_code == 400

def test_invalid_message_id():
    '''Test where message_id is an invalid string'''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token_0 = users_data[0]["token"]

    # send message to channel
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message":\
        "a"}).json()['message_id']


    response = requests.post(URL_MSG_REACT, json={"token": token_0, "message_id": "NOT_VALID_ID", \
        "message": "new_msg_1(1)"})
    assert response.status_code == 400 or response.status_code == 500

def test_user_not_in_channel():
    '''Test error occurs where user is not in the channel'''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # ch_id: owner = token_0; member = token_0, token_2
    # ch_id2: owner = token1; member = token_1
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "FOX_NEWS", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']

    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]
    token_2 = users_data[2]["token"]
    invite_user_channel(token_0, ch_id, users_data[2]['u_id'], URL_INVITE)

    # send 3 messages to each channel + 1 extra into channel2
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "a"}).json()['message_id']
    msg2_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "b"}).json()['message_id']
    msg3_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": \
        "c"}).json()['message_id']
    msg1_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": \
        "d"}).json()['message_id']
    msg2_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": \
        "e"}).json()['message_id']
    msg3_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": \
        "f"}).json()['message_id']

    # react to some messages where you arent in the channel
    response = requests.post(URL_MSG_REACT, json={"token": token_1, "message_id": msg1_1, \
        "react_id": 1})
    response2 = requests.post(URL_MSG_REACT, json={"token": token_0, "message_id": msg1_2, \
        "react_id": 1})
    response3 = requests.post(URL_MSG_REACT, json={"token": token_2, "message_id": msg1_2, \
        "react_id": 1})

    assert response.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400
