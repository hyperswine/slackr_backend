'''
This module only tests for channel_addowner.
Inputs = token, channel_id, u_id
Method = POST
'''
import requests

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET,\
    URL_REMOWNER, invite_user_channel, URL_INVITE, URL_DETAILS
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
    ok_ = common_set.add_user_owner(
        users_data[0]["token"], ch_id, users_data[2]["u_id"])

    assert ok_ == {}

    # send requeust to remove owner
    payload = requests.post(URL_REMOWNER, json={
        "token": users_data[0]["token"], "channel_id": ch_id, "u_id": users_data[2]["u_id"]}).json()

    # confirm output
    assert payload == {}

    token_ = users_data[0]["token"]

    # confirm that user[2] is no longer in owner_members
    payload = requests.get(
        URL_DETAILS + f'?token={token_}&channel_id={ch_id}').json()

    assert users_data[2]["u_id"] not in payload["owner_members"]


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

    # send a invite request
    invite_user_channel(
        users_data[0]["token"], ch_id, users_data[2]["u_id"], URL_INVITE)

    # add a user[2] as an owner
    common_set.add_user_owner(
        users_data[0]["token"], ch_id, users_data[2]["u_id"])

    # confirm http error, code = 404
    response = requests.post(URL_REMOWNER + '/', json={
        "token": users_data[0]["token"], "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 404


def test_errors():
    '''
    Testing for correct http error returns.
    Input = invalid route
    Expected Ouput = corresponding http error codes
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
    common_set.add_user_owner(
        users_data[0]["token"], ch_id, users_data[2]["u_id"])

    # confirm http error, code = 404
    # send base url
    response = requests.post(BASE_CHANNEL, json={
        "token": users_data[0]["token"], "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 404

    # confirm http error, code = 404
    # send base url appended with '/removal', i.e. a possible user mistake.
    response = requests.post(BASE_CHANNEL + '/removal', json={
        "token": users_data[0]["token"], "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 404

    # confirm http error, code = 405
    # send base url
    response = requests.get(URL_REMOWNER, json={
        "token": users_data[0]["token"], "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 405


def test_bad_data_rem_owner():
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

    # non-owner trying to remove himself as owner
    response = requests.post(URL_REMOWNER,
                             json={"token": users_data[2]["token"],
                                   "channel_id": ch_id, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 400

    # send invalid ch_id, which will result in an internal error
    response = requests.post(URL_REMOWNER,
                             json={"token": users_data[0]["token"],
                                   "channel_id": 124124, "u_id": users_data[2]["u_id"]})

    assert response.status_code == 400

    # send invalid u_id
    response = requests.post(URL_REMOWNER,
                             json={"token": users_data[0]["token"],
                                   "channel_id": ch_id, "u_id": "wow"})

    assert response.status_code == 400
