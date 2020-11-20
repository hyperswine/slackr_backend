from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import pytest as pt
import urllib.error
import flask
import requests

BASE_URL = 'http://localhost:8080'

def reset_workspace():
    request = Request(f"{BASE_URL}/workspace/reset",method = 'POST')
    urlopen(request)

@pt.fixture
def create_user1():
    reset_workspace()
    user1 = json.dumps({
        'name_first': 'great',
        'name_last': 'evenbetter',
        'email': 'Ecksdee@gmail.com',
        'password': 'greatevenbetter',
    }).encode('utf-8')
    
    request = Request(f"{BASE_URL}/auth/register", data=user1,headers={'Content-Type': 'application/json'},method= 'POST')
    
    return json.load(urlopen(request))

def test_basic(create_user1):
    
    user1 = create_user1
    
    assert user1 == {'u_id':user1['u_id'], 'token': user1['token']}
    
    name_data = json.dumps({
        'name_first': 'raymond',
        'name_last': 'tang',
        'token': user1['token']
    }).encode('utf-8')
    
    #PUT request to change users name.
    request = Request(f"{BASE_URL}/user/profile/setname", data=name_data, headers={'Content-Type': 'application/json'}, method='PUT')
    
    response = urlopen(request)
    
    query_string = urlencode({
        'u_id' : user1['u_id'],
        'token': user1['token']
    })
    
    #load the dictionary of user and see if the names were changed
    user1_info = json.load(urlopen(f"{BASE_URL}/user/profile?{query_string}"))
    
    #assert that it has the changed name
    
    assert user1_info['user']['name_first'] == 'raymond'
    
    assert user1_info['user']['name_last'] == 'tang'

def test_bad_data(create_user1):
    """First case of bad data when it throws an InputError is empty"""
    
    user1 = create_user1
    
    name_data = json.dumps({
        'name_first': '',
        'name_last': ''
    }).encode('utf-8')
    
    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/setname", data=name_data, headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(request)
   
    

def test_invalid_url(create_user1):
    """Tests that an invalid URL with correct data will throw an HTTPError """
    
    user1 = create_user1
    
    name_data = json.dumps({
        'name_first': 'validname',
        'name_last': 'validname'
    }).encode('utf-8')
    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/setnames", data=name_data, headers={'Content-Type': 'application/json'}, method='PUT')
        payload = urlopen(request)

def test_invalid_method(create_user1):
    """Tests that the putting in an invalid method will valid data will throw HTTPError"""
    
    user1 = create_user1
    
    name_data = json.dumps({
        'name_first': 'validname',
        'name_last': 'validname'
    }).encode('utf-8')

    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/setname", data=name_data, headers={'Content-Type': 'application/json'}, method='GET')
        response = urlopen(request)


