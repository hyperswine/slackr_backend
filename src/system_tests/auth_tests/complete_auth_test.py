'''
This is used to test all auth functions. We are putting it all in one
file as it is easier to handle registering -> logging out, and then
logging back in.
'''
import requests

from system_tests.fixtures.common_set import login_3_users, logout_3_users,\
 register_3_users, URL_RESET, BASE_AUTH, URL_REGISTER, URL_LOGIN, URL_LOGOUT,\
     user_0
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# Justifications: abides

###################
# REGISTER TESTS
###################

def test_basic():
    '''
    This is a sanity test for correct output based on all-correct input.
    Input = Correct email, password, first and last name.
    Expected Output = A dictionary containing u_id and token, with no errors.
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # confirm output
    assert users_data[0]["token"] and isinstance(users_data[0]["u_id"], int)
    assert users_data[1]["token"] and isinstance(users_data[1]["u_id"], int)
    assert users_data[2]["token"] and isinstance(users_data[2]["u_id"], int)


def test_route_name():
    '''
    This tests for inclusivity of '/' in the route url.
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    payload = requests.post(URL_REGISTER + '/', json={'email': 'pogchamp2@gmail.com',
                                                      'name_first': "xdlamoDsagf",
                                                      'name_last': "fondofpigsWgas",
                                                      'password': 'iamfondofpigs4'})

    # confirm output
    assert payload.status_code == 404


def test_errors():
    '''
    Testing for correct http error returns.
    Input = invalid route from auth
    Expected Ouput = corresponding http error codes
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    payload = requests.post(BASE_AUTH, json={'email': 'pogchamp2@gmail.com',
                                             'name_first': "xdlamoDsagf",
                                             'name_last': "fondofpigsWgas",
                                             'password': 'iamfondofpigs4'})

    # confirm output
    assert payload.status_code == 404

    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    payload = requests.post(BASE_AUTH + '/registration', json={'email': 'pogchamp2@gmail.com',
                                                               'name_first': "xdlamoDsagf",
                                                               'name_last': "fondofpigsWgas",
                                                               'password': 'iamfondofpigs4'})

    # confirm output
    assert payload.status_code == 404

    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    payload = requests.get(
        URL_REGISTER + '?email=pogchamp2@gmail.com&name_first=\
        xdlamoDsagf&name_last=fondofpigsWgas&password=iamfondofpigs4')

    # confirm output
    assert payload.status_code == 405


###################
# LOGOUT TESTS
###################

def test_basic_logout():
    '''
    This is a sanity test for correct output based on all-correct input.
    Input = Correct email, password, first and last name.
    Expected Output = A dictionary containing u_id and token, with no errors.
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    payload = requests.post(URL_LOGOUT, json={"token": users_data[0]["token"]})
    assert payload.json() == {"is_success": True}

    payload = requests.post(URL_LOGOUT, json={"token": users_data[1]["token"]})
    assert payload.json() == {"is_success": True}

    payload = requests.post(URL_LOGOUT, json={"token": users_data[2]["token"]})
    assert payload.json() == {"is_success": True}


def test_route_name_logout():
    '''
    This tests for inclusivity of '/' in the route url.
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    response = requests.post(
        URL_LOGOUT + '/', json={"token": users_data[0]["token"]})

    assert response.status_code == 404


def test_errors_logout():
    '''
    Testing for correct http error returns.
    Input = invalid route from auth
    Expected Ouput = corresponding http error codes
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    response = requests.post(BASE_AUTH, json={"token": users_data[0]["token"]})

    assert response.status_code == 404

    # reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    response = requests.post(BASE_AUTH + '/logouts',
                             json={"token": users_data[0]["token"]})

    assert response.status_code == 404

    # reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # use get method, which is invalid
    response = requests.get(URL_LOGOUT,
                            json={"token": users_data[0]["token"]})

    assert response.status_code == 405


def test_iterative_logout():
    '''
    This tests the behavior of logging out a lot of people continously and server load.
    '''

    #
    for _ in range(5):
        # reset the workspace
        requests.post(URL_RESET)

        # register 3 users
        users_data = register_3_users()

        # log them all out
        payload = requests.post(
            URL_LOGOUT, json={"token": users_data[0]["token"]})
        assert payload.json() == {"is_success": True}

        payload = requests.post(
            URL_LOGOUT, json={"token": users_data[1]["token"]})
        assert payload.json() == {"is_success": True}

        payload = requests.post(
            URL_LOGOUT, json={"token": users_data[2]["token"]})
        assert payload.json() == {"is_success": True}


################
# LOGIN TESTS
################

def test_basic_login():
    '''
    This is a sanity test for correct output based on all-correct input.
    Input = Correct email and password
    Expected Output = A dictionary containing u_id and token, with no errors.
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    logout_3_users([users_data[0]["token"], users_data[1]
                    ["token"], users_data[2]["token"]])

    # send request to log them in
    result = login_3_users()

    assert result[0]["token"] and isinstance(result[0]["u_id"], int)
    assert result[1]["token"] and isinstance(result[1]["u_id"], int)
    assert result[2]["token"] and isinstance(result[2]["u_id"], int)


def test_route_name_login():
    '''
    This tests for inclusivity of '/' in the route url.
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    logout_3_users([users_data[0]["token"], users_data[1]
                    ["token"], users_data[2]["token"]])

    # send request to log one of them in
    response = requests.post(URL_LOGIN + '/', json={
        "email": user_0["email"], "password": user_0["password"]})

    assert response.status_code == 404


def test_errors_login():
    '''
    Testing for correct http error returns.
    Input = invalid route from auth
    Expected Ouput = corresponding http error codes
    '''
    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    logout_3_users([users_data[0]["token"], users_data[1]
                    ["token"], users_data[2]["token"]])

    # send request to log one of them in
    response = requests.post(BASE_AUTH, json={
        "email": user_0["email"], "password": user_0["password"]})

    assert response.status_code == 404

    # first reset the workspace
    requests.post(URL_RESET)

    # register 3 users
    users_data = register_3_users()

    # log them all out
    logout_3_users([users_data[0]["token"], users_data[1]
                    ["token"], users_data[2]["token"]])

    # send request to log one of them in
    response = requests.post(BASE_AUTH + '/logins', json={
        "email": user_0["email"], "password": user_0["password"]})

    assert response.status_code == 404

    # send invalid method = GET
    response = requests.get(URL_LOGIN, json={
        "email": user_0["email"], "password": user_0["password"]})

    assert response.status_code == 405


def test_volatile_data_login():
    '''
    Confirm that the server can handle continous logins one-after-the-other
    '''
    for _ in range(15):
        # first reset the workspace
        requests.post(URL_RESET)

        # register 3 users
        users_data = register_3_users()

        # log them all out
        logout_3_users([users_data[0]["token"], users_data[1]
                        ["token"], users_data[2]["token"]])

        # send request to log them in
        result = login_3_users()

        assert result[0]["token"] and isinstance(result[0]["u_id"], int)
        assert result[1]["token"] and isinstance(result[1]["u_id"], int)
        assert result[2]["token"] and isinstance(result[2]["u_id"], int)
