'''
This stores the first set of fixtures to be used when pytest starts.
NOTE: run with python -m py.test for these tests to work properly.
'''
import requests
import json

# NOTE: If you are running the server on a different port, make sure to change this as well.
BASE = 'http://localhost:8080'

BASE_AUTH = BASE + '/auth'
BASE_ADMIN = BASE + '/admin'
BASE_CHANNEL = BASE + '/channel'
BASE_CHANNELS = BASE + '/channels'
BASE_USER = BASE + '/user'
BASE_USERS = BASE + '/users'
BASE_MESSAGE = BASE + '/message'
BASE_STANDUP = BASE + '/standup'
BASE_WORKSPACE = BASE + '/workspace'
BASE_SEARCH = BASE + '/search'

URL_LOGIN = BASE_AUTH + '/login'
URL_PERMISSIONS = BASE_ADMIN + '/userpermission/change'
URL_LOGOUT = BASE_AUTH + '/logout'
URL_ADDOWNER = BASE_CHANNEL + '/addowner'
URL_REMOWNER = BASE_CHANNEL + '/removeowner'
URL_DETAILS = BASE_CHANNEL + '/details'
URL_INVITE = BASE_CHANNEL + '/invite'
URL_MESSAGES = BASE_CHANNEL + '/messages'
URL_LEAVE = BASE_CHANNEL + '/leave'
URL_JOIN = BASE_CHANNEL + '/join'
URL_LIST = BASE_CHANNELS + '/list'
URL_LISTALL = BASE_CHANNELS + '/listall'
URL_CREATE = BASE_CHANNELS + '/create'
URL_PROFILE = BASE_USER + '/profile'
URL_SETNAME = URL_PROFILE + '/setname'
URL_SETEMAIL = URL_PROFILE + '/setemail'
URL_SETHANDLE = URL_PROFILE + '/sethandle'
URL_ALL = BASE_USERS + '/all'
URL_MSG_SEND = BASE_MESSAGE + '/send'
URL_MSG_SENDLATER = BASE_MESSAGE + '/sendlater'
URL_MSG_REACT = BASE_MESSAGE + '/react'
URL_MSG_UNREACT = BASE_MESSAGE + '/unreact'
URL_MSG_PIN = BASE_MESSAGE + '/pin'
URL_MSG_UNPIN = BASE_MESSAGE + '/unpin'
URL_MSG_REMOVE = BASE_MESSAGE + '/remove'
URL_MSG_EDIT = BASE_MESSAGE + '/edit'
URL_STNDUP_START = BASE_STANDUP + '/start'
URL_STNDUP_ACTIVE = BASE_STANDUP + '/active'
URL_STNDUP_SEND = BASE_STANDUP + '/send'
URL_SEARCH = BASE_SEARCH + '/search'
URL_RESET = BASE_WORKSPACE + '/reset'
URL_REGISTER = BASE_AUTH + '/register'

# 3 users to be registered.
user_0 = {
    'email': 'pogchamp@gmail.com',
    'name_first': "xdlamoD",
    'name_last': "fondofpigsW",
    'password': 'iamfondofpigs2'
}
user_1 = {
    'email': 'pogchamp1@gmail.com',
    'name_first': "xdlamoDfsa",
    'name_last': "fondofpigsWgq",
    'password': 'iamfondofpigs3'
}
user_2 = {
    'email': 'pogchamp2@gmail.com',
    'name_first': "xdlamoDsagf",
    'name_last': "fondofpigsWgas",
    'password': 'iamfondofpigs4'
}


# A function to register 3 users
def register_3_users():
    '''
    This sends a request to the server to register 3 users.

    Output - a tuple containing 3 dictionaries {"u_id", "token"}
    '''

    # Assuming register works as intended.
    result_0 = requests.post(URL_REGISTER, json=user_0)
    result_1 = requests.post(URL_REGISTER, json=user_1)
    result_2 = requests.post(URL_REGISTER, json=user_2)

    return (result_0.json(), result_1.json(), result_2.json())


# A function to log in the 3 users above
def login_3_users():
    '''
    Sends a request to server to login 3 users.

    Output - a tuple containing 3 dictionaries {"u_id", "token"}
    '''
    result_0 = requests.post(
        URL_LOGIN, json={"email": user_0["email"], "password": user_0["password"]})
    result_1 = requests.post(
        URL_LOGIN, json={"email": user_1["email"], "password": user_1["password"]})
    result_2 = requests.post(
        URL_LOGIN, json={"email": user_2["email"], "password": user_2["password"]})

    return (result_0.json(), result_1.json(), result_2.json())


# A function to log out the 3 users
def logout_3_users(tokens):
    '''
    Input - token
    Sends a request to server to logout 3 users.
    '''
    requests.post(URL_LOGOUT, json={"token": tokens[0]})
    requests.post(URL_LOGOUT, json={"token": tokens[1]})
    requests.post(URL_LOGOUT, json={"token": tokens[2]})


# Create a channel
def create_channel_99(token):
    '''
    Given user[0]'s token, create a channel with name = "FOX_NEWS" and is_public = True.

    Output - channel_id
    '''
    data_in = {"token": token, "name": "FOX_NEWS", "is_public": True}
    ch_id = requests.post(URL_CREATE, json=data_in).json()

    return ch_id["channel_id"]


# Invite a user to channel
def invite_user_channel(token, channel_id, u_id, URL_):
    '''
    Given the token of user[0], invite user[2], who is automatially added.

    Output - requests.post(URL_, data) json() object.
    '''
    data_in = {"token": token, "channel_id": channel_id, "u_id": u_id}
    return requests.post(URL_, json=data_in).json()


# Join a channel as a user
def join_as_user(token, channel_id):
    '''
    Given a token and a channel_id, join as the user with token.
    '''
    data_in = {"token": token, "channel_id": channel_id}
    requests.post(URL_JOIN, json=data_in)


# Add a user as an owner
def add_user_owner(token, channel_id, u_id):
    '''
    Given a channel owner's token, add u_id as an owner to channel.
    '''
    data_in = {"token": token, "channel_id": channel_id, "u_id": u_id}
    return requests.post(URL_ADDOWNER, json=data_in).json()


# Remove a user as an owner
def remove_user_owner(token, channel_id, u_id):
    pass


# Leave a channel
def leave_channel_user(token, channel_id):
    '''
    Given a user's token, leave him from the channel.
    '''
    data_in = {"token": token, "channel_id": channel_id}
    requests.post(URL_LEAVE, json=data_in)


# Global 3 messages data
messages_3 = [
    "I am fond of pigs. Dogs look up to us. Cats look down on us. Pigs treat us as equals.",

    "Give a man a fish, feed him for a day. Poison a man's fish, and you'll never have to feed him again.",

    "Maybe the real virus is human beings. We infect every corner of the planet and turn everything into factory, killing off other living things",
]


def send_3_messages(token, ch_id):
    '''
    Given the token of a channel member, send a message to the channel.
    '''
    response = requests.post(URL_MSG_SEND, json={
                  "token": token, "channel_id": ch_id, "message": messages_3[0]})
    assert response.status_code == 200
    response = requests.post(URL_MSG_SEND, json={
                  "token": token, "channel_id": ch_id, "message": messages_3[1]})
    assert response.status_code == 200
    response = requests.post(URL_MSG_SEND, json={
                  "token": token, "channel_id": ch_id, "message": messages_3[2]})
    assert response.status_code == 200
