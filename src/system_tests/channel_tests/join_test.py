'''
This module only tests for channel_join.
Inputs = token, channel_id
Method = POST
'''
import requests

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET, URL_JOIN


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

    # send a join request
    payload = requests.post(
        URL_JOIN, json={"token": users_data[1]["token"], "channel_id": ch_id})

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

    # send a join request
    response = requests.post(
        URL_JOIN+'/', json={"token": users_data[1]["token"], "channel_id": ch_id})

    assert response .status_code == 404


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

    # send a join request to base channel. if this doesnt raise an error,
    # there are serious problems with the implementation
    response = requests.post(
        BASE_CHANNEL+'/', json={"token": users_data[1]["token"], "channel_id": ch_id})

    assert response .status_code == 404

    # confirm http error, code = 404
    response = requests.post(
        BASE_CHANNEL+'/joining', json={"token": users_data[1]["token"], "channel_id": ch_id})

    assert response .status_code == 404

    # send with wrong method
    response = requests.get(
        URL_JOIN, json={"token": users_data[1]["token"], "channel_id": ch_id})

    assert response .status_code == 405


def test_bad_data_join():
    '''
    1. Sends an invalid token.
    2. Sends an invalid channel id.
    '''

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # send invalid token
    response = requests.post(
        URL_JOIN, json={"token": 1221451512, "channel_id": ch_id})

    assert response.status_code == 400

    # send invalid ch_id, which should result in a bad request
    response = requests.post(
        URL_JOIN, json={"token": users_data[0]["token"], "channel_id": 124124})

    assert response.status_code == 400
