'''
This module only tests for channel_addowner.
Inputs = token, channel_id
Method = POST
'''
import requests

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET,\
    URL_ADDOWNER, invite_user_channel, URL_INVITE
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# Justifications: abides


def test_basic():
    '''
    This is a sanity test for correct output based on all-correct input.
    Input = Correct token of owner, u_id of invitee and channel_id of owner.
    Expected Output = {} with no errors.
    '''

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # send a invite request
    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # add a user[2] as an owner
    payload = common_set.add_user_owner(
        users_data[0]["token"], ch_id, users_data[2]["u_id"])

    # confirm addowner output
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

    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    with requests.post(URL_ADDOWNER + '/', json={
            "token": users_data[0]["token"], "channel_id": ch_id,
            "u_id": users_data[2]["u_id"]}) as response:
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

    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # send base url
    common_set.add_user_owner(
        users_data[0]["token"], ch_id, users_data[2]["u_id"])
    response = requests.post(BASE_CHANNEL, json={
        "token": users_data[0]["token"], "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 404

    # send base url appended with '/adding'
    common_set.add_user_owner(
        users_data[0]["token"], ch_id, users_data[2]["u_id"])
    response = requests.post(BASE_CHANNEL + '/adding', json={
        "token": users_data[0]["token"], "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 404

    token = users_data[0]["token"]
    u_id = users_data[2]["u_id"]
    # send an invalid request
    common_set.add_user_owner(
        users_data[0]["token"], ch_id, users_data[2]["u_id"])
    response = requests.get(
        URL_ADDOWNER + f'?token={token}&channel_id={ch_id}&u_id={u_id}')


def test_bad_data_addowner():
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

    # non-owner trying to make himself the owner
    response = requests.post(URL_ADDOWNER,
                             json={"token": users_data[2]["token"],
                                   "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 400

    # send invalid ch_id, which will result in an internal error
    response = requests.post(URL_ADDOWNER,
                             json={"token": users_data[0]["token"],
                                   "channel_id": 124124, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 400

    # send invalid u_id
    response = requests.post(URL_ADDOWNER,
                             json={"token": users_data[0]["token"],
                                   "channel_id": ch_id, "u_id": "wow"})

    assert response.status_code == 400
