'''
This module only tests for channel_addowner.
Inputs = token, channel_id, start
Method = GET
'''
import requests

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_CHANNEL, URL_RESET,\
 send_3_messages, URL_MESSAGES, messages_3
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# Justifications: abides

def test_basic():
    '''
    This is a sanity test for correct output based on all-correct input.
    Input = Correct token, u_id and permission_id
    Expected Output = {} with no errors.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # send 3 messages to the channel
    send_3_messages(users_data[0]["token"], ch_id)

    token_ = users_data[0]["token"]

    # retrieve messages
    payload = requests.get(
        URL_MESSAGES + f"?token={token_}&channel_id={ch_id}&start={0}").json()

    # confirm output.
    assert payload["start"] == 0 and payload["end"] == -1
    assert payload["messages"][0]["message"] == messages_3[2]
    assert payload["messages"][1]["message"] == messages_3[1]
    assert payload["messages"][2]["message"] == messages_3[0]


def test_empty():
    '''
    Test an empty input.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])
    token_ = users_data[0]["token"]

    # retrieve messages
    payload = requests.get(
        URL_MESSAGES + f"?token={token_}&channel_id={ch_id}&start={0}").json()

    # confirm output.
    assert payload["start"] == 0 and payload["end"] == -1
    assert payload["messages"] == []


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

    # send 3 messages to the channel
    send_3_messages(users_data[0]["token"], ch_id)

    token_ = users_data[0]["token"]
    # retrieve messages
    response = requests.get(
        URL_MESSAGES + '/' + f"?token={token_}&channel_id={ch_id}&start={0}")

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

    # send 3 messages to the channel
    send_3_messages(users_data[0]["token"], ch_id)

    token_ = users_data[0]["token"]

    # retrieve messages
    response = requests.get(
        BASE_CHANNEL + f"?token={token_}&channel_id={ch_id}&start={0}")

    assert response.status_code == 404

    response = requests.get(
        BASE_CHANNEL + '/message' + f'?token={token_}&channel_id={ch_id}&start={0}')

    assert response.status_code == 404

    # confirm invalid method error
    response = requests.post(
        URL_MESSAGES + f"?token={token_}&channel_id={ch_id}&start={0}")

    assert response.status_code == 405


def test_bad_data_message():
    '''
    1. Sends a token of non-owner
    2. Sends an invalid channel id.
    3. Sends an invalid starting point
    '''

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    token_bad = users_data[2]["token"]
    token_ = users_data[0]["token"]

    # send a few messages
    send_3_messages(token_, ch_id)

    # send invalid token
    response = requests.get(
        URL_MESSAGES + f"?token={token_bad}&channel_id={ch_id}&start={0}")
    assert response.status_code == 400

    # send invalid ch_id, which should result in a bad request
    response = requests.get(
        URL_MESSAGES + f"?token={token_}&channel_id={125521}&start={0}")
    assert response.status_code == 400

    # send invalid starting point
    response = requests.get(
        URL_MESSAGES + f"?token={token_}&channel_id={ch_id}&start={5000}")
    assert response.status_code == 400
