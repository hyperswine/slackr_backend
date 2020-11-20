from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import pytest as pt
import urllib.error
import flask
import requests

"""sethandle system tests"""

"""HTTP Route {BASE_URL}/user/sethandle"""

"""PUT method"""

BASE_URL = 'http://localhost:8080'

def reset_workspace():
    request = Request(f"{BASE_URL}/workspace/reset",method = 'POST')
    urlopen(request)

@pt.fixture
def user1():
    reset_workspace()
    user1 = json.dumps({
        'name_first': 'great',
        'name_last': 'evenbetter',
        'email': 'Ecksdee@gmail.com',
        'password': 'greatevenbetter',
    }).encode('utf-8')
    
    request = Request(f"{BASE_URL}/auth/register", data=user1,headers={'Content-Type': 'application/json'},method= 'POST')
    
    return json.load(urlopen(request))



def test_basic(user1):
    """Basic test to update a users handle"""
    
    handle_data = json.dumps({
        'handle_str': 'newhandle',
        'token': user1['token']
    }).encode('utf-8')
    
    response = Request(f"{BASE_URL}/user/profile/sethandle", data=handle_data, headers={'Content-Type': 'application/json'}, method='PUT')
    payload = urlopen(response)
    
    #Check if the handle string was updated using the get method.
    query_string = urlencode({
        'u_id' : user1['u_id'],
        'token': user1['token']
    })
    
    user1_info = json.load(urlopen(f"{BASE_URL}/user/profile?{query_string}"))
    
    #assert that it has the changed handle
    assert user1_info['user']['handle_str'] == 'newhandle'

def test_bad_data(user1):
    """First case of bad data is if the handle string is empty (Because handle string needs to be 2 - 20)"""
    
    handle_data = json.dumps({
        'handle_str': ''
    }).encode('utf-8')
    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/sethandle", data=handle_data, headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(request)

def test_wrong_url(user1):
    """Test to raise a HTTPError when url is entered wrongly"""

    handle_data = json.dumps({
        'handle_str': 'validhandle'
    }).encode('utf-8')

    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/sethandles", data=handle_data, headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(request)

def test_wrong_method(user1):
    """Test to raise HTTPError when Method is entered wrongly"""
  
    handle_data = json.dumps({
        'handle_str': 'validhandle'
    }).encode('utf-8')
    
    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/sethandle", data=handle_data, headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(request)

