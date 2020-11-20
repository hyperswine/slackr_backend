import pytest
import app.auth as auth
import app.channel as channel
import app.channels as channels
import app.message as message
from main.error import InputError, AccessError
from app.workspace import workspace_reset
import app.search as search
# pylint: disable=E1136
# Justification for disabling => see pylint issues/3139


def create_user():
    workspace_reset()
    return auth.register("test@test.com", "password123", "Test", "User")


def test_search1():
    testUser = create_user()
    testChannel = channels.create(testUser['token'], "Test Channel", True)
    message.send(testUser['token'], testChannel['channel_id'], "Hello World")
    message.send(testUser['token'], testChannel['channel_id'], "Bye World")
    message.send(testUser['token'], testChannel['channel_id'], "Hello Dux Wu")
    message.send(testUser['token'], testChannel['channel_id'], "WuHan cool")
    result = search.search(testUser['token'], "Wu")
    
    # Don't know what order the result list is
    assert (result['messages'][0]['message'] == 'Hello Dux Wu' and result['messages'][1]['message'] == 'WuHan cool')\
        or (result['messages'][0]['message'] == 'WuHan cool' and result['messages'][1]['message'] == 'Hello Dux Wu')


def test_search_multi_channel():
    testUser = create_user()
    testChannel = channels.create(testUser['token'], "Test Channel", True)
    testChannel2 = channels.create(testUser['token'], "Test Channel2", True)
    message.send(testUser['token'], testChannel['channel_id'], "Hello World")
    message.send(testUser['token'], testChannel2['channel_id'], "Bye World")
    message.send(testUser['token'], testChannel2['channel_id'], "Hello Dux Wu")
    message.send(testUser['token'], testChannel2['channel_id'], "WuHan cool")
    result = search.search(testUser['token'], "World")
    result2 = search.search(testUser['token'], "Wu")

    assert (result['messages'][0]['message'] == 'Hello World' and result['messages'][1]['message'] == 'Bye World')\
        or (result['messages'][0]['message'] == 'Bye World' and result['messages'][1]['message'] == 'Hello World')

    assert (result2['messages'][0]['message'] == 'Hello Dux Wu' and result2['messages'][1]['message'] == 'WuHan cool')\
        or (result2['messages'][1]['message'] == 'WuHan cool' and result2['messages'][0]['message'] == 'Hello Dux Wu')


# No matches
def test_search_no_match():
    testUser = create_user()
    testChannel = channels.create(testUser['token'], "Test Channel", True)
    message.send(testUser['token'], testChannel['channel_id'], "Hello World")
    message.send(testUser['token'], testChannel['channel_id'], "Bye World")
    message.send(testUser['token'], testChannel['channel_id'], "Hello Dux Wu")
    message.send(testUser['token'], testChannel['channel_id'], "WuHan cool")
    result = search.search(testUser['token'], "Ayaya")
    
    assert result == {'messages': []}


# No messages, expected no matches
def test_search_no_mesages():
    testUser = create_user()
    testChannel = channels.create(testUser['token'], "Test Channel", True)
    result = search.search(testUser['token'], "#toiletpapercrisis")
    
    assert result == {'messages': []}
