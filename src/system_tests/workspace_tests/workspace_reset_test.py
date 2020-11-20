'''
This module only tests for workspace reset.
'''
import requests
import json
import pytest as pt
import pdb

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import URL_STNDUP_START, send_3_messages, BASE_CHANNEL, URL_RESET, URL_ADDOWNER, invite_user_channel, URL_INVITE

def test_basic_reset():
    '''
    Send a variety of data to the server, then reset and confirm that all the data has been cleared.
    - Register users -> user_data
    - Create channel with owner -> all_channels
    - Send a message -> message_data
    - Start a standup -> standup_list
    Confirm that all these datasets are free
    '''
    # reset workspace
    response = requests.post(URL_RESET)

    assert response.json() == {}

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # send a invite request to user[2]
    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # send a message as the owner
    send_3_messages(users_data[0]["token"], ch_id)

    token_ = users_data[0]["token"]

    # start a standup, lasting for 30 seconds maximum
    requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                  "channel_id": ch_id, "length": 30})

    # send a standup message
    requests.post(URL_STNDUP_START, json={"token": token_,
                  "channel_id": ch_id, "length": 5})
    
    # reset the workspace
    requests.post(URL_RESET)

    assert response.json() == {}

    # confirm that all workspace data has been cleared


def test_name_route_reset():
    '''
    Tests for appending / at the end of url
    '''
    # reset workspace
    response = requests.post(URL_RESET+ '/')

    # confirm we get 404
    assert response.status_code == 404


def test_errors_reset():
    '''
    Tests for various http errors and confirm non-redirection behavior
    '''
    # attempt reset at base url
    response = requests.post('http://localhost:8080/workspace')

    # confirm we get 404
    assert response.status_code == 404

    # attempt reset at something similar to true url
    response = requests.post('http://localhost:8080/workspace/resetting')

    # confirm we get 404
    assert response.status_code == 404

    # attempt reset at something similar to true url 2nd version
    response = requests.post('http://localhost:8080/workspace/resets')

    # confirm we get 404
    assert response.status_code == 404

    # request with wrong method GET
    response = requests.get(URL_RESET)
