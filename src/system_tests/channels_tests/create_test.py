import urllib.request
import json
import pytest as pt
import requests
from system_tests.fixtures.common_set import URL_RESET

BASE_URL = 'http://localhost:8080'

def create_user_data(name_first,name_last,email,password):
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

#Most basic to create a channel POST
def test_basic():
     # reset workspace
    requests.post(URL_RESET)
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)
    #POST method
    channel_data = json.dumps({
        'token' : user1['token'],
        'name' : 'greatchannel',
        'is_public' : True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=channel_data,headers={'Content-Type': 'application/json'},method= 'POST')
    #user1 is already in the channel
    payload = json.load(urllib.request.urlopen(req))
    #this is a dictionary of {channel_id : ' '}

    #Want to make sure the channel is created by using list_channels

    query_string = urllib.parse.urlencode({
        'token': user1['token']
    }).encode('utf-8')

    response = urllib.request.urlopen(f"{BASE_URL}/channels/listall?token={user1['token']}")
    payload2 = json.load(response)
    #this should be a list of dictionaries of channel form  { 'channels' :
    assert payload2 == { 'channels' :
                                    [{
                                    'channel_id': payload['channel_id'],
                                    'name': 'greatchannel'
                                    }]
                        }
def test_bad_url():
    """Test of wrong URL should throw a http error"""
    # reset workspace
    requests.post(URL_RESET)
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)

    channel_data = json.dumps({
        'token' : user1['token'],
        'name' : 'greatchannel',
        'is_public' : True
    }).encode('utf8')

    response = urllib.request.Request(f"{BASE_URL}/channel/create", data=channel_data,headers={'Content-Type': 'application/json'},method= 'POST')

    with pt.raises(urllib.error.HTTPError):
        urllib.request.urlopen(response)

def test_bad_data():
     # reset workspace
    requests.post(URL_RESET)
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)

    channel_data = json.dumps({
        'token' : user1['token'],
        'name' : 'thisnameiswayyyyyyyytooooooooooolonggggggggggggggg',
        'is_public' : True
    }).encode('utf8')

    response = urllib.request.Request(f"{BASE_URL}/channels/create", data=channel_data,headers={'Content-Type': 'application/json'},method= 'POST')

    with pt.raises(urllib.error.HTTPError):
        urllib.request.urlopen(response)

def test_wrong_method():
     # reset workspace
    requests.post(URL_RESET)
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)

    channel_data = json.dumps({
        'token' : user1['token'],
        'name' : 'thisnameiswayyyyyyyytooooooooooolonggggggggggggggg',
        'is_public' : True
    }).encode('utf8')

    response = urllib.request.Request(f"{BASE_URL}/channels/create", data=channel_data,headers={'Content-Type': 'application/json'},method= 'GET')

    with pt.raises(urllib.error.HTTPError):
        urllib.request.urlopen(response)






