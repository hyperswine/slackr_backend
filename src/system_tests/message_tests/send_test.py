'''
This module only tests for message/send.
'''
import urllib
import requests
from datetime import datetime, timezone
import json
import pytest as pt
import pdb
import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET, URL_ADDOWNER, invite_user_channel, URL_INVITE, send_3_messages, URL_MESSAGES, messages_3, URL_CREATE, URL_PROFILE, URL_MSG_SEND


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

    # send 3 messages to each channel + 1 extra into channel2
    send_3_messages(users_data[0]["token"], ch_id)
    send_3_messages(users_data[1]["token"], ch_id2)
    
    token_0 = users_data[0]["token"]
    token_1 = users_data[1]["token"]

    requests.post(URL_MSG_SEND, json={"token": token_1, "channel_id": ch_id2, "message": "another message"})

    # retrieve messages
    payload = requests.get(
        URL_MESSAGES + f"?token={token_0}&channel_id={ch_id}&start=0").json()
    payload2 = requests.get(
        URL_MESSAGES + f"?token={token_1}&channel_id={ch_id2}&start=0").json()
    # confirm output.
    assert payload["start"] == 0 and payload["end"] == -1
    assert payload["messages"][2]["message"] == messages_3[0]
    assert payload["messages"][1]["message"] == messages_3[1]
    assert payload["messages"][0]["message"] == messages_3[2]

    assert payload2["start"] == 0 and payload2["end"] == -1
    assert payload2["messages"][3]["message"] == messages_3[0]
    assert payload2["messages"][2]["message"] == messages_3[1]
    assert payload2["messages"][1]["message"] == messages_3[2]
    assert payload2["messages"][0]["message"] == "another message"

    assert isinstance(payload["messages"][0]["u_id"], int) 
    assert isinstance(payload2["messages"][0]["u_id"], int) 
    assert payload["messages"][0]["u_id"] != payload2["messages"][0]["u_id"]

    # assert timestamp is within 60 seconds of the time now.
    assert abs(payload["messages"][0]['time_created'] - (datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())) < 60
    assert abs(payload2["messages"][0]['time_created'] - (datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())) < 60

    assert abs(payload['messages'][0]['is_pinned']) == False

    # unable to check reacts becuase don't know how many react ids there are

def test_invalid_token():
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create 2 channels
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "FOX_NEWS", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']

    # send 3 messages to each channel + 1 extra into channel2
    response = requests.post(URL_MSG_SEND, json={"token": "NOT_VALID_TOKEN", "channel_id": ch_id2, "message": "another message"})
    assert response.status_code == 400

def test_user_not_in_channel():
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create 2 channels
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    data_in = {"token": users_data[1]["token"], "name": "new", "is_public": True}
    ch_id2 = requests.post(URL_CREATE, json=data_in).json()['channel_id']

    # send 3 messages to channels which users are not in.
    
    response = requests.post(URL_MSG_SEND, json={"token": users_data[1]['token'], "channel_id": ch_id, "message": "another message"})
    response2 = requests.post(URL_MSG_SEND, json={"token": users_data[2]["token"], "channel_id": ch_id2, "message": "another message"})

    assert response.status_code == 400
    assert response2.status_code == 400
    