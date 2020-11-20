'''
This module only tests for channel_details.
Inputs = token, channel_id.
Method = GET
'''
import requests

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET,\
    URL_ADDOWNER, invite_user_channel, URL_INVITE, URL_DETAILS
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

    # invite users to channel
    invite_user_channel(users_data[0]["token"],
                        ch_id, users_data[1]["u_id"], URL_INVITE)
    invite_user_channel(users_data[0]["token"],
                        ch_id, users_data[2]["u_id"], URL_INVITE)

    token = users_data[0]["token"]

    # send a details request
    payload = requests.get(
        URL_DETAILS + f'?token={token}&channel_id={ch_id}').json()

    # confirm output
    assert payload["name"] == "FOX_NEWS"
    assert payload["owner_members"] and payload["all_members"]


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

    # invite users to channel
    invite_user_channel(users_data[0]["token"],
                        ch_id, users_data[1]["u_id"], URL_INVITE)
    invite_user_channel(users_data[0]["token"],
                        ch_id, users_data[2]["u_id"], URL_INVITE)

    token = users_data[0]["token"]

    response = requests.get(
        URL_DETAILS + '/' + f'?token={token}&channel_id={ch_id}')

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

    token = users_data[0]["token"]

    # confirm http error, code = 404
    # send base url
    response = requests.get(
        BASE_CHANNEL + f'?token={token}&channel_id={ch_id}')

    assert response.status_code == 404

    # confirm http error, code = 404
    # send base url with 'detail'
    response = requests.get(
        BASE_CHANNEL + '/detail' + f'?token={token}&channel_id={ch_id}')

    assert response.status_code == 404

    # confirm http error, code = 405
    # send with post method, i.e. not get.
    response = requests.post(URL_DETAILS, json={
        "token": token, "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 405


def test_bad_data_details():
    '''
    1. Sends a token of a non owner.
    2. Sends an invalid channel id.
    '''

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token = users_data[1]["token"]

    # non-owner trying to get channel details
    response = requests.get(
        URL_DETAILS + f'?token={token}&channel_id={ch_id}')

    assert response.status_code == 400

    # send invalid ch_id
    response = requests.post(URL_ADDOWNER,
                             json={"token": users_data[0]["token"],
                                   "channel_id": 124124, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 400
