'''
This module only tests for message/unpin
'''
import requests
import urllib
from datetime import datetime, timezone
import json
import pytest as pt
import pdb
import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET, URL_ADDOWNER, \
    invite_user_channel, URL_INVITE, send_3_messages, URL_MESSAGES, messages_3, URL_CREATE, \
    URL_PROFILE, URL_MSG_SEND, URL_MSG_PIN, URL_MSG_UNPIN


def test_basic():
    '''
    This is a sanity test for correct output based on all-correct input.
    '''
    # debug mode
    # pdb.set_trace()

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]
    token_2 = users_data[2]["token"]

    # owner of slackr = token_0
    # ch_id: owner = token_0; member = token_0, token_2
    # ch_id2: owner = token1; member = token_1
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "FOX_NEWS", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']
    invite_user_channel(token_0, ch_id, users_data[2]['u_id'], URL_INVITE)


    # send 3 messages to each channel + 1 extra into channel2
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "a"}).json()['message_id']
    msg2_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "b"}).json()['message_id']
    msg3_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "c"}).json()['message_id']
    msg1_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "d"}).json()['message_id']
    msg2_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "e"}).json()['message_id']
    msg3_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "f"}).json()['message_id']
    
    # pin some messages - first is owner of channel and slackr, second is owner of channel, third is owner of slackr
    requests.post(URL_MSG_PIN, json={"token": token_0, "message_id": msg1_1})
    requests.post(URL_MSG_PIN, json={"token": token_1, "message_id": msg1_2})
    requests.post(URL_MSG_PIN, json={"token": token_0, "message_id": msg3_2})

    # unpin the messages - first is owner of channel and slackr, second is owner of channel, third is owner of slackr
    requests.post(URL_MSG_UNPIN, json={"token": token_0, "message_id": msg1_1})
    requests.post(URL_MSG_UNPIN, json={"token": token_1, "message_id": msg1_2})
    requests.post(URL_MSG_UNPIN, json={"token": token_0, "message_id": msg3_2})
    
    # retrieve messages
    payload = requests.get(
        URL_MESSAGES + f"?token={token_0}&channel_id={ch_id}&start=0").json()
    payload2 = requests.get(
        URL_MESSAGES + f"?token={token_1}&channel_id={ch_id2}&start=0").json()
    
    
    # confirm output.
    assert payload["messages"][0]["is_pinned"] == False
    assert payload["messages"][1]["is_pinned"] == False
    assert payload2["messages"][0]["is_pinned"] == False
    assert payload2["messages"][2]["is_pinned"] == False

def test_already_unpinned():
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token_0 = users_data[0]["token"]

    # send message to channel
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "a"}).json()['message_id']

    response = requests.post(URL_MSG_UNPIN, json={"token": token_0, "message_id": msg1_1})
    assert response.status_code == 400

def test_invalid_message_id():
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token_0 = users_data[0]["token"]

    # send message to channel
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "a"}).json()['message_id']


    response = requests.post(URL_MSG_UNPIN, json={"token": token_0, "message_id": "NOT_VALID_ID", "message": "new_msg_1(1)"})
    assert response.status_code == 400 or response.status_code == 500

def test_user_not_in_channel():
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]
    token_2 = users_data[2]["token"]

    # ch_id: owner = token_0; member = token_0, token_2
    # ch_id2: owner = token1; member = token_1
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "FOX_NEWS", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']
    invite_user_channel(token_0, ch_id, users_data[2]['u_id'], URL_INVITE)

    # send 3 messages to each channel + 1 extra into channel2
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "a"}).json()['message_id']
    msg2_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "b"}).json()['message_id']
    msg3_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "c"}).json()['message_id']
    msg1_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "d"}).json()['message_id']
    msg2_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "e"}).json()['message_id']
    msg3_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "f"}).json()['message_id']

    # pin some messages
    requests.post(URL_MSG_PIN, json={"token": token_0, "message_id": msg1_1})
    requests.post(URL_MSG_PIN, json={"token": token_1, "message_id": msg1_2})
    requests.post(URL_MSG_PIN, json={"token": token_0, "message_id": msg3_2})

    # unpin some messages where you arent in the channel
    response = requests.post(URL_MSG_UNPIN, json={"token": token_1, "message_id": msg1_1})
    response = requests.post(URL_MSG_UNPIN, json={"token": token_2, "message_id": msg1_2})

    assert response.status_code == 400

def test_user_not_owner_of_slackr_or_channel():
        # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]
    token_2 = users_data[2]["token"]

    # ch_id: owner = token_0; member = token_0, token_2
    # ch_id2: owner = token1; member = token_1
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "FOX_NEWS", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']
    invite_user_channel(token_0, ch_id, users_data[2]['u_id'], URL_INVITE)


    # send 3 messages to each channel + 1 extra into channel2
    msg1_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "a"}).json()['message_id']
    msg2_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "b"}).json()['message_id']
    msg3_1 = requests.post(URL_MSG_SEND, json={"token": token_0, "channel_id": ch_id, "message": "c"}).json()['message_id']
    msg1_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "d"}).json()['message_id']
    msg2_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "e"}).json()['message_id']
    msg3_2 = requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "f"}).json()['message_id']
    
    requests.post(URL_MSG_PIN, json={"token": token_0, "message_id": msg1_1})
    requests.post(URL_MSG_PIN, json={"token": token_2, "message_id": msg1_2})
    requests.post(URL_MSG_PIN, json={"token": token_0, "message_id": msg3_2})

    # unpin some messages where you arent owner of channel or slackr
    response = requests.post(URL_MSG_UNPIN, json={"token": token_2, "message_id": msg1_1})
    assert response.status_code == 400