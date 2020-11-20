'''
This module only tests for all standup functions.
Start: token, ch_id, len. POST. {time_finish}
Active: token, ch_id. GET. {is_active, time_finish}
Send: token, ch_id, message. POST. {}.
'''
import requests
import json
import pytest as pt
import pdb
from datetime import timezone, datetime, time
from time import sleep

import system_tests.fixtures.common_set as common_set
from system_tests.fixtures.common_set import BASE_STANDUP, URL_STNDUP_START,\
    URL_STNDUP_SEND, URL_STNDUP_ACTIVE, URL_ADDOWNER,\
    invite_user_channel, URL_INVITE, messages_3, URL_RESET, URL_MESSAGES


def test_basic_start():
    '''
    Start a standup in a channel with valid inputs.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds
    result = requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                                   "channel_id": ch_id, "length": 30}).json()

    # Use this to confirm time finish > now
    # now_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()

    # confirm return
    assert isinstance(result["time_finish"], int)


def test_start_route_name():
    '''
    Test functionality of appending a '/' to the route.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds
    result = requests.post(URL_STNDUP_START + '/', json={"token": users_data[0]["token"],
                                                         "channel_id": ch_id, "length": 30})

    assert result.status_code == 404


def test_errors_start():
    '''
    Tests possible redirection routes that shouldn't be implemented.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds
    result = requests.post(BASE_STANDUP, json={"token": users_data[0]["token"],
                                               "channel_id": ch_id, "length": 30})

    assert result.status_code == 404

    # request a standup for 30 seconds
    result = requests.post(BASE_STANDUP + '/starting', json={"token": users_data[0]["token"],
                                                             "channel_id": ch_id, "length": 30})

    assert result.status_code == 404

    # request a standup for 30 seconds
    result = requests.post(BASE_STANDUP + '/starts', json={"token": users_data[0]["token"],
                                                           "channel_id": ch_id, "length": 30})

    assert result.status_code == 404

    # confirm invalid method result.
    result = requests.get(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                                  "channel_id": ch_id, "length": 30})

    assert result.status_code == 405


def test_bad_input_start():
    '''
    1. Send token of non-owner
    2. Send invalid channel_id
    3. Send invalid length
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds by user[1]
    result = requests.post(URL_STNDUP_START, json={"token": users_data[1]["token"],
                                                   "channel_id": ch_id, "length": 30})

    assert result.status_code == 400

    # request a standup for 30 seconds in an invalid channel
    result = requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                                   "channel_id": 12251251, "length": 30})

    assert result.status_code == 400

    # request a standup for 30 seconds with an invalid length
    result = requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                                   "channel_id": ch_id, "length": -55})

    assert result.status_code == 400


################
# ACTIVE TESTS
################

def test_active_basic():
    '''
    Confirm we get the correct output on valid input and start standup.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # start a standup for 30 seconds
    result = requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                                   "channel_id": ch_id, "length": 30}).json()

    token_ = users_data[0]["token"]

    # req if standup is active
    response = requests.get(
        URL_STNDUP_ACTIVE + f'?token={token_}&channel_id={ch_id}').json()

    assert response["is_active"]
    assert response["time_finish"] == result["time_finish"]


def test_non_owner_active():
    '''
    Given a non-owner's token, confirm that he can check if a given
    channel has a standup active
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # check if a standup is active with non channel member user[1]
    token_bad = users_data[1]["token"]
    token_ = users_data[0]["token"]

    response = requests.get(
        URL_STNDUP_ACTIVE + f'?token={token_bad}&channel_id={ch_id}')

    assert response.status_code == 200


def test_active_route_name():
    '''
    Confirm http error upon appendation of backslash.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds
    requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                          "channel_id": ch_id, "length": 30}).json()

    token_ = users_data[0]["token"]

    # req if standup is active
    response = requests.get(URL_STNDUP_ACTIVE + '/' +
                            f'?token={token_}&channel_id={ch_id}')

    assert response.status_code == 404


def test_errors_active():
    '''
    Confirm http error upon appendation of backslash.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds
    requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                          "channel_id": ch_id, "length": 30}).json()

    token_ = users_data[0]["token"]

    # req if standup is active
    response = requests.get(
        BASE_STANDUP + f'?token={token_}&channel_id={ch_id}')

    assert response.status_code == 404

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds
    requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                          "channel_id": ch_id, "length": 30})

    token_ = users_data[0]["token"]

    # req if standup is active at 'actives'
    response = requests.get(BASE_STANDUP + '/actives' +
                            f'?token={token_}&channel_id={ch_id}')

    assert response.status_code == 404

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # request a standup for 30 seconds
    requests.post(URL_STNDUP_START, json={"token": users_data[0]["token"],
                                          "channel_id": ch_id, "length": 30})

    token_ = users_data[0]["token"]

    # req if standup is active with invalid POST method
    response = requests.post(
        URL_STNDUP_ACTIVE + f'?token={token_}&channel_id={ch_id}')

    assert response.status_code == 405


def test_bad_input_active():
    '''
    1. Send invalid token
    2. Send invalid channel_id
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # check if a standup is active with non channel member user[1]
    token_bad = 215125125125
    token_ = users_data[0]["token"]

    response = requests.get(
        URL_STNDUP_ACTIVE + f'?token={token_bad}&channel_id={ch_id}')

    assert response.status_code == 400

    # check if standup is active in a non-existent channel
    response = requests.get(
        URL_STNDUP_ACTIVE + f'?token={token_}&channel_id={52521125}')

    assert response.status_code == 400


################
# STANDUP SEND
################

def test_basic_send():
    '''
    Start a standup and send a message to it.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    token_ = users_data[0]["token"]

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(token_)

    # request a standup for 30 seconds
    requests.post(URL_STNDUP_START, json={"token": token_,
                                          "channel_id": ch_id, "length": 5})

    # send 3 messages
    response = requests.post(URL_STNDUP_SEND, json={
                             "token": token_, "channel_id": ch_id, "message": messages_3[0]})
    assert response.json() == {}

    response = requests.post(URL_STNDUP_SEND, json={
                             "token": token_, "channel_id": ch_id, "message": messages_3[1]})
    assert response.json() == {}

    response = requests.post(URL_STNDUP_SEND, json={
                             "token": token_, "channel_id": ch_id, "message": messages_3[2]})
    assert response.json() == {}

    # confirm that these messages will be in the channel after 3 seconds
    sleep(5)

    result = requests.get(
        URL_MESSAGES + f"?token={token_}&channel_id={ch_id}&start={0}").json()
    # confirm output.
    assert result["start"] == 0 and result["end"] == -1
    assert result["messages"][0]["message"] == "\nxdlamoDfondofpigsW: I am fond of pigs. Dogs look up to us. Cats look down on us. Pigs treat us as equals.\nxdlamoDfondofpigsW: Give a man a fish, feed him for a day. Poison a man's fish, and you'll never have to feed him again.\nxdlamoDfondofpigsW: Maybe the real virus is human beings. We infect every corner of the planet and turn everything into factory, killing off other living things"


def test_route_name_send():
    '''
    Send message to appended / url.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    token_ = users_data[0]["token"]

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(token_)

    # request a standup for 30 seconds
    requests.post(URL_STNDUP_START, json={"token": token_,
                                          "channel_id": ch_id, "length": 5}).json()

    # send 3 messages
    response = requests.post(
        URL_STNDUP_SEND + '/', json={"token": token_, "channel_id": ch_id, "message": messages_3[0]})
    assert response.status_code == 404


def test_errors_send():
    '''
    Send message to appended / url.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    token_ = users_data[0]["token"]

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(token_)

    # request a standup for 30 seconds
    requests.post(URL_STNDUP_START, json={"token": token_,
                                          "channel_id": ch_id, "length": 10}).json()

    # send to base url
    response = requests.post(BASE_STANDUP, json={
                             "token": token_, "channel_id": ch_id, "message": messages_3[0]})
    assert response.status_code == 404

    # send to to sending
    response = requests.post(BASE_STANDUP + '/sending',
                             json={"token": token_, "channel_id": ch_id, "message": messages_3[0]})
    assert response.status_code == 404

    # send to to sent
    response = requests.post(
        BASE_STANDUP + '/sent', json={"token": token_, "channel_id": ch_id, "message": messages_3[0]})
    assert response.status_code == 404

    # send with wrong method
    response = requests.get(
        URL_STNDUP_SEND + f"?token={token_}&channel_id={ch_id}&message={messages_3[0]}")
    assert response.status_code == 405


def test_bad_input_send():
    '''
    1. Send invalid token
    2. Send invalid channel_id
    3. Send a message '**5000, too long.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = common_set.register_3_users()

    # create a channel with user[0] as the owner
    ch_id = common_set.create_channel_99(users_data[0]["token"])

    # check if a standup is active with non channel member user[1]
    token_bad = 215125125125
    token_ = users_data[0]["token"]

    # send message with invalid token
    response = requests.post(URL_STNDUP_SEND, json={
                             "token": token_bad, "channel_id": ch_id, "message": messages_3[0]})
    assert response.status_code == 400

    # send message with invalid channel_id
    response = requests.post(URL_STNDUP_SEND, json={
                             "token": token_, "channel_id": 125125132, "message": messages_3[0]})

    assert response.status_code == 400

    # send a huge message
    response = requests.post(URL_STNDUP_SEND, json={
                             "token": token_, "channel_id": ch_id, "message": 'a'*1001})

    assert response.status_code == 400
