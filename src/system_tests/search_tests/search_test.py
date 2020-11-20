import urllib.error
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import pytest as pt
import requests
import flask

"""search system tests"""

"""HTTP Route {BASE_URL}/search"""

"""GET method"""

COMPLETE_URL = 'http://localhost:8000/search'

BASE_URL = 'http://localhost:8000'

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
    "create the channel"
    data_in = {'token': user1['token'], 'name': 'FOX_NEWS', 'is_public': True}
    ch_id = requests.post(URL_CREATE, json=data_in).json()

    messages_3 = [
        "I am fond of pigs. Dogs look up to us. Cats look down on us. Pigs treat us as equals.",

        "Give a man a fish, feed him for a day. Poison a man's fish, and you'll never have to feed him again.",

        "Maybe the real virus is human beings. We infect every corner of the planet and turn everything into factory, killing off other living things",
    ]

    response1 = requests.post(URL_MSG_SEND, json={
        'token': user1['token'], 'channel_id': ch_id, 'message': messages_3[0]})

    response2 = requests.post(URL_MSG_SEND, json={
        'token': user1['token'], 'channel_id': ch_id, 'message': messages_3[1]})

    response3 = requests.post(URL_MSG_SEND, json={
        'token': user1['token'], 'channel_id': ch_id, 'message': messages_3[2]})

    user1_messages = requests.get(f"{BASE_URL}/search?token={user1['token']}&query_str=Pigs").json()['user']

    assert user1_messages['messages'][0]['message'] == messages_3[0]

def test_bad_token(user1):
    query_string = urlencode({
        'token': 'wqjenwqkjen',
        'query_str': 'Pigs'
    })

    with pt.raises(urllib.error.HTTPError):
        #Raises error when HTTP is opened
        urlopen(f"{BASE_URL}/search?{query_string}")

def test_bad_url(user1):
    query_string = urlencode({
        'token': user1['token'],
        'query_str': 'Pigs'
    })

    with pt.raises(urllib.error.HTTPError):
        urlopen(f"{BASE_URL}/user/searches?{query_string}")

def test_basic2(user1):
    "create the channel"
    data_in = {'token': user1['token'], 'name': 'FOX_NEWS', 'is_public': True}
    ch_id = requests.post(URL_CREATE, json=data_in).json()
    data_in2 = {'token': user1['token'], 'name': 'FOX_NEWS2', 'is_public': True}
    ch_id2 = requests.post(URL_CREATE, json=data_in2).json()

    messages_3 = [
        "I am fond of a certain pig. Dogs look up to us. Cats look down on us. Pigs treat us as equals.",

        "Give a man a fish, feed him for a day. Poison a man's fish, and you'll never have to feed him again.",

        "Maybe the real virus is human beings. We infect every corner of the planet and turn everything into factory, killing off other living things",

        "Spiderpig spiderpig does whatever spiderpig does, can he swing from a web, no he can't he's a pig.",
    ]

    response1 = requests.post(URL_MSG_SEND, json={
        'token': user1['token'], 'channel_id': ch_id, 'message': messages_3[0]})

    response2 = requests.post(URL_MSG_SEND, json={
        'token': user1['token'], 'channel_id': ch_id, 'message': messages_3[1]})

    response3 = requests.post(URL_MSG_SEND, json={
        'token': user1['token'], 'channel_id': ch_id, 'message': messages_3[2]})

    response4 = requests.post(URL_MSG_SEND, json={
        'token': user1['token'], 'channel_id': ch_id2, 'message': messages_3[3]})

    user1_messages = requests.get(f"{BASE_URL}/search?token={user1['token']}&query_str=pig").json()['user']

    assert user1_messages['messages'][0]['message'] == messages_3[0]
    assert user1_messages['messages'][1]['message'] == messages_3[3]
