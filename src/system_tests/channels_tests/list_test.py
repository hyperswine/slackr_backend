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
    """Function to create the user, returns a dictionary of their u_id and token"""
    #Sends a HTTP Request to auth/register to get
    response = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, headers={'Content-Type': 'application/json'},method= 'POST')
    #changes output to something we can manipulate
    result = json.load(urllib.request.urlopen(response))
    return result

def create_channel_data(token,name,is_public):
    """Returns the data wrapped in json"""
    return json.dumps({
        'token' : token,
        'name' : name,
        'is_public' : is_public
    }).encode('utf-8')

def create_channel(channel_data):
    """
    Function which creates the channel
    Returns a dictionary of their {channel_id: }
    """

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=channel_data, headers={'Content-Type': 'application/json'},method= 'POST')
    payload = json.load(urllib.request.urlopen(req))
    return payload

def test_basic():
    """Basic test where it is the user is part of 2 channels one private and one not and returns both"""
    # reset workspace
    requests.post(URL_RESET)
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)

    channel_data_pub = create_channel_data(user1['token'],'nicename',True)
    channel_data_priv = create_channel_data(user1['token'],'notnicename',False)

    pub_channel = create_channel(channel_data_pub)
    priv_channel = create_channel(channel_data_priv)

    query_string = urllib.parse.urlencode({
        'token' : user1['token']
    })

    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={user1['token']}")
    payload = json.load(response)
    #List of channels

    assert payload == {'channels' :
                                    [{
                                    'channel_id': pub_channel['channel_id'],
                                    'name': 'nicename'
                                    },
                                    {
                                    'channel_id': priv_channel['channel_id'],
                                    'name': 'notnicename'
                                    }]
                        }
def test_basic2():
    # reset workspace
    requests.post(URL_RESET)
    """Tests where there is other channels that the user is not part of"""
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)

    user2_data = create_user_data('notnice', 'notnicer', 'notnice@gmail.com', 'sjandkjwqnd')
    user2 = create_user(user2_data)

    channel_data1 = create_channel_data(user1['token'],'nicename',True)
    channel_data2 = create_channel_data(user2['token'], 'noice', True)

    channel1 = create_channel(channel_data1)
    channel2 = create_channel(channel_data2)

    query_string = urllib.parse.urlencode({
        'token': user1['token']
    })

    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?token={user1['token']}")
    payload = json.load(response)

    assert payload == { 'channels' :
                                    [{
                                    'channel_id': channel1['channel_id'],
                                    'name': 'nicename'
                                    }]
                        }
def test_bad_url():
    # reset workspace
    requests.post(URL_RESET)
    """Test that it throws an error for bad url"""
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)

    channel_data1 = create_channel_data(user1['token'],'nicename',True)
    channel1 = create_channel(channel_data1)

    query_string = urllib.parse.urlencode({
        'token': user1['token']
    })
    with pt.raises(urllib.error.HTTPError):
       urllib.request.urlopen(f"{BASE_URL}/channel/list?{query_string}")

def test_invalid_token():
    # reset workspace
    requests.post(URL_RESET)
    user1_data = create_user_data('nice', 'evennicer', 'nice@gmail.com', 'wqjneqwkjen')
    user1 = create_user(user1_data)

    channel_data1 = create_channel_data(user1['token'],'nicename',True)
    channel1 = create_channel(channel_data1)

    with pt.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channels/list?token=aeorghoireagjioe")




