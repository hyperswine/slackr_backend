'''
This module only tests for channel_invite.
Inputs = token, channel_id, u_id
Method = POST
'''
import requests

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET,\
 invite_user_channel, URL_INVITE
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# Justifications: abides

def test_basic():
    '''
    Test correct input -> output
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # send an invite request
    payload = invite_user_channel(users_data[0]["token"],
                                  ch_id, users_data[1]["u_id"], URL_INVITE)

    # confirm output
    assert payload == {}


def test_route_name():
    '''
    This tests for inclusivity of '/' in the route url.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # send an invite request
    response = requests.post(URL_INVITE + '/', data={"token": users_data[0]["token"],
                                                     "channel_id": ch_id, "u_id": users_data[1]["u_id"]})

    # confirm 404
    assert response.status_code == 404


def test_errors():
    '''
    Testing for correct http error returns.
    Input = invalid route from admin
    Expected Ouput = corresponding http error codes
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # send an invite request to user[2]
    response = requests.post(BASE_CHANNEL, data={"token": users_data[0]["token"],
                                                 "channel_id": ch_id, "u_id": users_data[1]["u_id"]})

    # confirm 404
    assert response.status_code == 404

    # send an invite request to user[2]
    response = requests.post(BASE_CHANNEL + '/invites', data={"token": users_data[0]["token"],
                                                              "channel_id": ch_id, "u_id": users_data[1]["u_id"]})

    # confirm 404
    assert response.status_code == 404

    # confirm http error, code = 405
    # send an invite request to user[2]
    response = requests.get(URL_INVITE, data={"token": users_data[0]["token"],
                                              "channel_id": ch_id, "u_id": users_data[1]["u_id"]})

    # confirm 404
    assert response.status_code == 405


def test_bad_data_invite():
    '''
    1. Sends a token of a non owner.
    2. Sends an invalid channel id.
    3. Sends an invalid u_id.
    '''

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    
    # send an invite request to user[1]
    invite_user_channel(users_data[0]["token"],
                                  ch_id, users_data[1]["u_id"], URL_INVITE)


    # non-owner user[1] trying to invite user[2]
    response = requests.post(URL_INVITE, json={"token": users_data[1]["token"], "channel_id": 124124, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 400

    # send invalid ch_id, which will result in an internal error
    response = requests.post(URL_INVITE, json={"token": users_data[1]["token"], "channel_id": 124124, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 400

    # send invalid u_id
    response = requests.post(URL_INVITE, json={"token": users_data[1]["token"], "channel_id": ch_id, "u_id": 12551})

    assert response.status_code == 400
