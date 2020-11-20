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

@pt.fixture()
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
    """Tests basic function of setemail"""
    
    user1 = create_user1

    email_data = json.dumps({
        'email': 'newemail@gmail.com',
        'token': user1['token']
    }).encode('utf-8')
    
    #Updates the email of the user
    request = Request(f"{BASE_URL}/user/profile/setemail", data=email_data, headers={'Content-Type': 'application/json'}, method='PUT')
    
    #Grab the payload, and change if we dont need it
    payload = urlopen(request)
    
    query_string = urlencode({
        'u_id' : user1['u_id'],
        'token': user1['token']
    })
    
    user1_info = json.load(urlopen(f"{BASE_URL}/user/profile?{query_string}"))
    
    #assert that it has the changed email
    assert user1_info['user']['email'] == 'newemail@gmail.com'

def test_invalid_email(create_user1):
    """Invalid email should through an input error which should throw a HTTPError"""
    user1 = create_user1
    
    email_data = json.dumps(
    {
        'token': user1['token'],
        'email': 'a.gmail.com',
    }).encode('utf-8')
    
    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/setemail", data=email_data, headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(request)
    

def test_invalid_url(create_user1):
    """Tests that entering an invalid url will throw a HTTPError"""
    user1 = create_user1
    
    email_data = json.dumps({
        'token': user1['token'],
        'email': '@ahah@gmail.com'
    }).encode('utf-8')
    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/setemails", data=email_data, headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(request)

def test_invalid_method(create_user1):
    """Tests that using the wrong method will throw a HTTPError"""
    user1 = create_user1
    
    email_data = json.dumps({
        'email': '@gmail.com'
    }).encode('utf-8')

    with pt.raises(urllib.error.HTTPError):
        request = Request(f"{BASE_URL}/user/profile/setemail", data=email_data, headers={'Content-Type': 'application/json'}, method='PUT')
        response = urlopen(request)
