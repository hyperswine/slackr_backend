'''
This is only used to test 'change_permissions', which is a POST route.
'''
import requests

from system_tests.fixtures.common_set import URL_RESET, \
    URL_PERMISSIONS, BASE_ADMIN, register_3_users
# pylint: disable=bad-continuation
# pylint: disable=line-too-long
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# Justifications for pylint ignore => pep8 style guides.


def test_basic():
    '''
    This is a sanity test for correct output based on all-correct input.
    Input = Correct token, u_id and permission_id
    Expected Output = {} with no errors.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = register_3_users()

    # send request with p_id 1
    payload = requests.post(URL_PERMISSIONS, json={
                            "token": users_data[0]["token"], "u_id": users_data[1]["u_id"], "permission_id": 1})

    # confirm output
    assert payload.json() == {}

    # send request with p_id 2
    payload = requests.post(URL_PERMISSIONS, json={
                            "token": users_data[0]["token"], "u_id": users_data[1]["u_id"], "permission_id": 2})

    # confirm output
    assert payload.json() == {}


def test_route_name():
    '''
    This tests for inclusivity of '/' in the route url.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = register_3_users()

    # send request with p_id 1
    response = requests.post(URL_PERMISSIONS + '/', json={
        "token": users_data[0]["token"], "u_id": users_data[1]["u_id"], "permission_id": 1})

    # confirm output
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
    users_data = register_3_users()

    # send request with p_id 1
    response = requests.post(BASE_ADMIN, json={
        "token": users_data[0]["token"], "u_id": users_data[1]["u_id"], "permission_id": 1})

    # confirm output
    assert response.status_code == 404

    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = register_3_users()

    # send request with p_id 1
    response = requests.post(BASE_ADMIN + '/permissions', json={
        "token": users_data[0]["token"], "u_id": users_data[1]["u_id"], "permission_id": 1})

    # confirm output
    assert response.status_code == 404

    token = users_data[0]["token"]
    u_id = users_data[1]["u_id"]

    # send to with wrong method
    response = requests.get(
        URL_PERMISSIONS + f'?token={token}&u_id={u_id}&permission_id={1}')

    # confirm output
    assert response.status_code == 405


def test_volatile_data():
    '''
    Since data.py gets dumped to data.p every 3 seconds, this function tests the behavior of the timing of dumping.

    It sends data to the complete route every 3.1 seconds and verifies that the data has not been lost or placed somewhere it shouldn't be.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = register_3_users()

    # iterate 10 times to ensure we didnt lose anything.
    for _ in range(10):
        payload = requests.post(URL_PERMISSIONS, json={
            "token": users_data[0]["token"], "u_id": users_data[1]["u_id"], "permission_id": 2})
        assert payload.json() == {}


def test_bad_input():
    '''
    1. Send invalid token.
    2. Send token of non-owner and try to make himself slackr owner.
    3. Send invalid u_id.
    4. Send invalid permission id.
    '''
    # reset workspace
    requests.post(URL_RESET)

    # register 3 people, fetch tokens and u_id of the users.
    users_data = register_3_users()

    # send request with p_id 1
    payload = requests.post(URL_PERMISSIONS, json={
                            "token": 45125125, "u_id": users_data[1]["u_id"], "permission_id": 1})

    # confirm error
    assert payload.status_code == 400

    # send request with non slackr owner
    payload = requests.post(URL_PERMISSIONS, json={
                            "token": users_data[1]["token"], "u_id": users_data[1]["u_id"], "permission_id": 1})

    # confirm error
    assert payload.status_code == 400

    # send request with invalid u_id
    payload = requests.post(URL_PERMISSIONS, json={
                            "token": users_data[0]["token"], "u_id": 125125, "permission_id": 1})

    # confirm error
    assert payload.status_code == 400

    # send request with invalid permission_id
    payload = requests.post(URL_PERMISSIONS, json={
                            "token": users_data[0]["token"], "u_id": users_data[0]["u_id"], "permission_id": 3})

    # confirm error
    assert payload.status_code == 400
