import urllib.request
import urllib.error
import urllib.parse
import json
import pytest as pt
import requests
from system_tests.fixtures.common_set import URL_RESET
"""Users all test"""
"""GET Method"""

BASE_URL = 'http://localhost:8080'

def create_data(name_first,name_last,email,password):
    return json.dumps({
        'name_first': name_first,
        'name_last': name_last,
        'email': email,
        'password': password,
    }).encode('utf-8')

def create_user(data):
    #Sends a HTTP Request to auth/register to get
    response = urllib.request.Request(f"{BASE_URL}/auth/register", data=data,headers={'Content-Type': 'application/json'},method= 'POST')
    #changes output to something we can manipulate
    result = json.load(urllib.request.urlopen(response))
    return result
    #Result is a dictionary in the form of {'u_id': , 'token': }

def test_basic():
    # reset workspace
    requests.post(URL_RESET)
    user_data = create_data('great','evenbetter','Ecksdee@gmail.com','asaaaaadfg')
    user1 = create_user(user_data)
    #Query string for user 1
    query_string = urllib.parse.urlencode({
        'u_id' : user1['u_id'],
        'token': user1['token']
    })

    user_dictionary  = json.load(urllib.request.urlopen(f"{BASE_URL}/users/all?{query_string}"))
    user1_info = json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query_string}"))
    assert user_dictionary == {
        'users': [
            user1_info['user']
        ]
    }
def test_multiple():
    """Second basic test where there are multiple users"""
    # reset workspace
    requests.post(URL_RESET)
    user_data1 = create_data('great','evenbetter','Ecksdee@gmail.com','asaaaaaaadfg')
    user_data2 = create_data('nice', 'evennicer', 'ECKSDEEEE@gmail.com','sadjaaaawqnd')
    user1 = create_user(user_data1)
    #Query string for user 1
    user2 = create_user(user_data2)
    query_string1 = urllib.parse.urlencode({
        'u_id' : user1['u_id'],
        'token': user1['token']
    })
    query_string2 = urllib.parse.urlencode({
        'u_id': user2['u_id'],
        'token': user2['token']
    })
    #Users dictionary from perspective of user 1

    #Dictionary for the first user
    user1_info = json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query_string1}"))
    #Dictionary for the second user
    user2_info = json.load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{query_string2}"))
    user1_dictionary = json.load(urllib.request.urlopen(f"{BASE_URL}/users/all?{query_string1}"))
    user2_dictionary = json.load(urllib.request.urlopen(f"{BASE_URL}/users/all?{query_string2}"))
    assert user1_dictionary == {
        'users': [
            user1_info['user'],
            user2_info['user']
        ]
    }
    assert user2_dictionary == {
        'users': [
            user1_info['user'],
            user2_info['user']
        ]
    }

def test_bad_token():
    # reset workspace
    requests.post(URL_RESET)
    user_data1 = create_data('great','evenbetter','Ecksdee@gmail.com','asaaaaadfg')
    user1 = create_user(user_data1)

    query_string1 = urllib.parse.urlencode({
        'u_id' : user1['u_id'],
        'token': 'INVALIDTOKEN'
    }).encode('utf8')

    with pt.raises(urllib.error.HTTPError):
       urllib.request.urlopen(f"{BASE_URL}/user/all?{query_string1}")

def test_bad_url():
    # reset workspace
    requests.post(URL_RESET)
    with pt.raises(urllib.error.HTTPError):
       urllib.request.urlopen(f"{BASE_URL}/user/all?u_id=12409124819&token=1234812eogiarh")






