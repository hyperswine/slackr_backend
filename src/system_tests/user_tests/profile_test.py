from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import pytest as pt
import urllib.error
import flask
import requests

"""user_profile system tests"""

"""HTTP Route {BASE_URL}/user/profile"""

"""GET method"""

BASE_URL = 'http://localhost:8080'    

def reset_workspace():
    requests.post(f"{BASE_URL}/workspace/reset")

@pt.fixture
def user1():
    reset_workspace()
    user_1 = {
        'name_first' : 'great',
        'name_last' : 'evenbetter',
        'email' : 'Ecksdee@gmail.com',
        'password' : 'greatevenbetter'
    }
    
    result_0 = requests.post(f"{BASE_URL}/auth/register", json=user_1).json()
    return result_0


def test_basic(user1):
    """Tests that with a valid user, user_profile will return the given user's dictionary
    INPUTS = token u_id"""

    user1_info = requests.get(f"{BASE_URL}/user/profile?u_id={user1['u_id']}&token={user1['token']}").json()['user']
    assert user1_info['name_first'] == 'great'
    assert user1_info['name_last'] == 'evenbetter'
    assert isinstance(user1_info['u_id'], int)
    assert user1_info['email'] == 'Ecksdee@gmail.com'
    assert user1_info['handle_str'] == 'greatevenbetter'


def test_invalid_token(user1):
    assert user1 == {'u_id': user1['u_id'], 'token': user1['token']}
    
    query_string = urlencode({
        'u_id': user1['u_id'],
        'token': 'wqjenwqkjen',
    })
    
    with pt.raises(urllib.error.HTTPError):
       #Raises error when HTTP is opened
       urlopen(f"{BASE_URL}/user/profile?{query_string}")


def test_invalid_user_id(user1):
    assert user1 == {'u_id': user1['u_id'], 'token': user1['token']}
    
    query_string = urlencode({
        'u_id': 'qwqwqw',
        'token': user1['token'],
    })
    
    with pt.raises(urllib.error.HTTPError):
       #Raises error when HTTP is opened
       urlopen(f"{BASE_URL}/user/profile?{query_string}")

def test_invalid_token2(user1):
    assert user1 == {'u_id': user1['u_id'], 'token': user1['token']}
    
    query_string = urlencode({
        'u_id': user1['u_id'],
        'token': 'INVALID_TOKEN'
    })
    
    with pt.raises(urllib.error.HTTPError):
        urlopen(f"{BASE_URL}/user/profile?{query_string}")
      
def test_wrong_url(user1):
    query_string = urlencode({
        'u_id' : user1['u_id'],
        'token': user1['token']
    })
    
    with pt.raises(urllib.error.HTTPError):
       urlopen(f"{BASE_URL}/user/profiles?{query_string}")

