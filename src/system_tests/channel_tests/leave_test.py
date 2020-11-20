'''
This module only tests for channel_leave.
Inputs = token, channel_id
Method = POST
'''
import requests

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET,\
    invite_user_channel, URL_INVITE, URL_LEAVE
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

    # invite user to channel
    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # send a leave request
    payload = requests.post(
        URL_LEAVE, json={"token": users_data[2]["token"], "channel_id": ch_id})

    # confirm output
    assert payload.json() == {}


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

    # invite user to channel
    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # send a leave request
    response = requests.post(
        URL_LEAVE+'/', json={"token": users_data[2]["token"], "channel_id": ch_id})

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

    # invite user to channel
    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # send a leave request
    response = requests.post(
        BASE_CHANNEL, json={"token": users_data[2]["token"], "channel_id": ch_id})

    assert response.status_code == 404

    # send a join request to base channel. if this doesnt raise an error,
    # there are serious problems with the implementation
    response = requests.post(
        BASE_CHANNEL+'/', json={"token": users_data[2]["token"], "channel_id": ch_id})

    assert response.status_code == 404

    response = requests.post(
        BASE_CHANNEL+'/leaving', json={"token": users_data[2]["token"], "channel_id": ch_id})

    assert response.status_code == 404

    # send with wrong method
    response = requests.get(
        URL_LEAVE, json={"token": users_data[2]["token"], "channel_id": ch_id})

    assert response.status_code == 405


def test_bad_data_leave():
    '''
    1. Sends token of a non-member.
    2. Sends an invalid channel id.
    '''

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # invite 2 people
    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # send invalid token
    response = requests.post(
        URL_LEAVE, json={"token": users_data[1]["token"], "channel_id": ch_id})

    assert response.status_code == 400

    # send invalid ch_id with ownr, which should result in bad request
    response = requests.post(URL_LEAVE, json={"token": users_data[0]["token"],
                                              "channel_id": 124124})

    assert response.status_code == 400

    # send invalid ch_id with user[1], which should result in bad request
    response = requests.post(URL_LEAVE, json={"token": users_data[1]["token"],
                                              "channel_id": 124124})

    assert response.status_code == 400
