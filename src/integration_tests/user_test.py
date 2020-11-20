#Setting up and housekeeping for the tests
#imports
#start with importing all files to make life easier.
import app.auth as auth
import app.channel as channel
import app.channels as channels
from main.error import InputError, AccessError
from app.workspace import workspace_reset
import app.message as message
from app.user import profile, setemail, sethandle, setname, all_
import pytest


#helper functions
#Create a VALID user, which are logged in.
def create_user():
    workspace_reset()
    return auth.register('Example@example.com', 'Example', 'John', 'Smith')

def create_user2():
    return auth.register('Example2@example2.com', 'Example2', 'Donaldo', 'Trumpu')


#Assumption that generation of handle string is correct.
#For a valid user, returns user dictionary.
def test_user_profile01():
    new_user = create_user()
    user_dictionary = { 
        'user': {
            'u_id': new_user['u_id'],
            'email': 'Example@example.com',
            'name_first': 'John',
            'name_last': 'Smith', 'profile_img_url': 'http://127.0.0.1:8080/profileimages/default.jpg',
            'handle_str' : 'JohnSmith'
        }
    }
    #Makes sure the profile returns the user_dictionary.
    assert profile(new_user['token'],new_user['u_id']) == user_dictionary


#profile test02: tests a user with an invalid user ID.
def test_user_profile02(): 
    new_user = create_user()
    with pytest.raises(InputError):
        profile(new_user['u_id'], 000000000000)
    #raises error when ID is invalid


#profile test3: Tests a user with an invalid user token.
def test_user_profile03():
    new_user = create_user()
    with pytest.raises(AccessError):
        profile('NOT_VALID_TOKEN', new_user['u_id'])


#Assumption that generation of handle string is correct.
#For a valid user, returns user dictionary. (multiple users)
def test_user_profile05():
    new_user = create_user()
    new_user2 = create_user2()
    user_dictionary = { 
        'user': {
            'u_id': new_user['u_id'],
            'email': 'Example@example.com',
            'name_first': 'John2',
            'name_last': 'Smith2',
            'handle_str' : 'JohnSmith'
        }
    }
    user_dictionary2 = { 
        'user': {
            'u_id': new_user2['u_id'],
            'email': 'Example2@example2.com',
            'name_first': 'Donaldo',
            'name_last': 'Trumpu',
            'handle_str' : 'donaldotrumpu'
        }
    }
    #Makes sure the profile returns the correct user_dictionary.
    assert profile(new_user['token'],new_user['u_id']) == user_dictionary
    assert profile(new_user2['token'],new_user2['u_id']) == user_dictionary2


#Assumption that generation of handle string is correct.
#For a valid user, returns user dictionary. (multiple users, checking the details of users users)
def test_user_profile06():
    new_user = create_user()
    new_user2 = create_user2()
    user_dictionary = { 
        'user': {
            'u_id': new_user['u_id'],
            'email': 'Example@example.com',
            'name_first': 'John2',
            'name_last': 'Smith2',
            'handle_str' : 'JohnSmith'
        }
    }
    user_dictionary2 = { 
        'user': {
            'u_id': new_user2['u_id'],
            'email': 'Example2@example2.com',
            'name_first': 'Donaldo',
            'name_last': 'Trumpu',
            'handle_str' : 'donaldotrumpu'
        }
    }
    #Makes sure the profile returns the correct user_dictionary.
    assert profile(new_user2['token'],new_user['u_id']) == user_dictionary
    assert profile(new_user['token'],new_user2['u_id']) == user_dictionary2


#profile test01: Tests that profile setname updates users first and 
#last name.
def test_setname01():
    new_user = create_user()
    #changes first name to Citizen, and last name to Slopsmcgee
    setname(new_user['u_id'],"Citizen","Slopsmcgee")
   
    new_user_dictionary = { #Dictionary with new information
        "user": {
            "u_id": new_user['u_id'],
            "email": 'Example@example.com',
            "name_first": "Citizen",
            "name_last": "Slopsmcgee",
            "handle_str": "JohnSmith"
        }
    }

    assert profile(new_user['token'],new_user['u_id']) == new_user_dictionary


#profile test02: Tests that profile setname updates only first name.
def test_setname02():
    new_user = create_user()
    #changes first name to Citizen
    setname(new_user['u_id'],"Citizen","Smith")
   
    new_user_dictionary = { #Dictionary with updated first name
        "user": {
            "u_id": new_user['u_id'],
            "email": 'Example@example.com',
            "name_first": "Citizen",
            "name_last": "Smith",
            "handle_str": "JohnSmith"
        }
    }
    #assert they are the same
    assert profile(new_user['token'],new_user['u_id']) == new_user_dictionary


#profile test03: Tests that profile setname updates only last name.
def test_setname03():
    new_user = create_user()
    #changes and last name to Slopsmcgee
    setname(new_user['u_id'],"John","Slopsmcgee")
   
    new_user_dictionary = { #Dictionary with new information
        "user": {
            "u_id": new_user['u_id'],
            "email": 'Example@example.com',
            "name_first": "John",
            "name_last": "Slopsmcgee",
            "handle_str": "JohnSmith"
        }
    }
    #assert they are the same
    assert profile(new_user['token'],new_user['u_id']) == new_user_dictionary


#setname04: Tests >50 character name_first and valid name_last.
def test_setname04():
    new_user = create_user()
    with pytest.raises(InputError):
        setname(new_user['u_id'], 'b' * 51, "Slopsmcgee")


#setname05: Tests > 50 character name_last, and valid name_first.
def test_setname05():
    new_user = create_user()
    with pytest.raises(InputError):
        setname(new_user['u_id'], 'Steven', 's' * 51)


#setname06: Tests < 1 character name_first, and valid name_last.
def test_setname06():
    new_user = create_user()
    with pytest.raises(InputError):
        setname(new_user['u_id'], 'b' * 0, "Slopsmcgee")


#setname07: Tests < 1 character name_last, and a valid name_first.
def test_setname07():
    new_user = create_user()
    with pytest.raises(InputError):
        setname(new_user['u_id'], 'Steven', 's' * 0)


#setname08: Tests 50 character name_last (just short enough), and valid name_first.
def test_setname08():
    new_user = create_user()
    setname(new_user['u_id'], 'Steven', 's' * 50)
    new_user_dictionary = { #Dictionary with new information
        "user": {
            "u_id": new_user['u_id'],
            "email": 'Example@example.com',
            "name_first": "Steven",
            "name_last": "s" * 50,
            "handle_str": "JohnSmith"
        }
    }
    assert profile(new_user['token'],new_user['u_id']) == new_user_dictionary


#setname09: Tests 1 character name_last (just long enough), and valid name_first.
def test_setname09():
    new_user = create_user()
    setname(new_user['u_id'], 'Steven', 's')
    new_user_dictionary = { #Dictionary with new information
        "user": {
            "u_id": new_user['u_id'],
            "email": 'Example@example.com',
            "name_first": "Steven",
            "name_last": "s",
            "handle_str": "JohnSmith"
        }
    }
    assert profile(new_user['token'],new_user['u_id']) == new_user_dictionary


#setname10: Tests 50 character name_first (just short enough), and valid name_first.
def test_setname10():
    new_user = create_user()
    setname(new_user['u_id'], 's' * 50, 'Smith')
    new_user_dictionary = { #Dictionary with new information
        "user": {
            "u_id": new_user['u_id'],
            "email": 'Example@example.com',
            "name_first": "s" * 50,
            "name_last": "Smith",
            "handle_str": "JohnSmith"
        }
    }
    assert profile(new_user['token'],new_user['u_id']) == new_user_dictionary


#setname11: Tests 1 character name_first (just long enough), and valid name_first.
def test_setname11():
    new_user = create_user()
    setname(new_user['u_id'], 's', 'Smith')
    new_user_dictionary = { #Dictionary with new information
        "user": {
            "u_id": new_user['u_id'],
            "email": 'Example@example.com',
            "name_first": "s",
            "name_last": "Smith",
            "handle_str": "JohnSmith"
        }
    }
    assert profile(new_user['token'],new_user['u_id']) == new_user_dictionary


#setname10: Changing name with an invalid u_id
def test_setname12():
    new_user = create_user()
    with pytest.raises(InputError):
        setname(000000000000, 'Steven', 's' * 5)


#setemail01: Given an authorised user, updates their email address.
def test_setemail01():
    new_user = create_user()
    setemail(new_user['token'],"Slopsmcgee@gmail.com")
    new_user_dictionary = {
        "u_id": new_user['u_id'],
        "email": 'Slopsmcgee@gmail.com',
        "name_first": "John",
        "name_last": "Smith",
        "handle_str": "JohnSmith"
    }
    assert profile(new_user['token'],['u_id']) == new_user_dictionary


#setemail02: Tests New Email with no personal info
def test_setemail02():
    new_user = create_user()
    #New Email with no personal info
    with pytest.raises(InputError):
        setemail(new_user['token'],'@gmail.com')


#setemail03: Tests New Email with no domain
def test_setemail03():
    new_user = create_user()
    with pytest.raises(InputError):
        setemail(new_user['token'],'gmail.com')


#setemail04: Tests New Email with no @  
def test_setemail04():
    new_user = create_user()
    with pytest.raises(InputError):
        setemail(new_user['token'],'gmailgmail.com')


#setemail05: Test changing to an already in use email.
def test_setemail05():
    test_user = auth.register("Test@test.com", "Test", "John", "Smith")
    new_user = create_user()
    #New_user will be trying to change their email to test_
    with pytest.raises(InputError):
        setemail(new_user['token'],'Test@test.com')


#setemail06: Test access error for setemail
def test_setemail06():
    new_user = create_user()
    with pytest.raises(AccessError):
        setemail('NOT_VALID_TOKEN','test@test.com')


#sethandle01: Given an authorised user, changes their handle_str
def test_sethandle01():
    new_user = create_user()
    sethandle(new_user['token'],"newhandle")
    new_user_dictionary = {
        "user": {
            "u_id" : new_user["u_id"],
            "email" : "Example@example.com",
            "name_first" : "John",
            "name_last" : "Smith",
            "handle_str": "newhandle"
        }
    }
    assert new_user_dictionary == profile(new_user['token'],new_user['u_id'])


#sethandle02: Tests < 3 character handle
def test_sethandle02():
    new_user = create_user()
    with pytest.raises(InputError):
        sethandle(new_user['token'],'aa')


#sethandle03: tests > 20 character handle
def test_sethandle03():
    new_user = create_user()
    with pytest.raises(InputError):
        sethandle(new_user['token'],'a' * 20)


#sethandle04: Tests = 3 character handle
def test_sethandle04():
    new_user = create_user()
    sethandle(new_user['token'],"aaa")
    new_user_dictionary = {
        "user": {
            "u_id" : new_user["u_id"],
            "email" : "Example@example.com",
            "name_first" : "John",
            "name_last" : "Smith",
            "handle_str": "aaa"
        }
    }
    assert new_user_dictionary == profile(new_user['token'],new_user['u_id'])


#sethandle05: Tests = 20 character handle
def test_sethandle05():
    new_user = create_user()
    sethandle(new_user['token'],"a" * 20)
    new_user_dictionary = {
        "user": {
            "u_id" : new_user["u_id"],
            "email" : "Example@example.com",
            "name_first" : "John",
            "name_last" : "Smith",
            "handle_str": "a" * 20
        }
    }
    assert new_user_dictionary == profile(new_user['token'],new_user['u_id'])


#CHECK TEST
#sethandle06: Tests changing handle_str into another users.
def test_sethandle06():
    new_user = create_user()
    test_user = auth.register('Test@test.com','Test', 'John', 'Smith')
    with pytest.raises(InputError):
        sethandle(new_user['token'],test_user['handle_str'])


#sethandle07: Tests Accesserror for changing the handle_str 
def test_sethandle07():
    with pytest.raises(AccessError):
        sethandle('NOT_VALID_TOKEN','randomhandle')


#USERS_ALL TESTS Assumptions: returns all users in the server (not channel)
#Users do not have to be logged in
#profile works.
#test_user_all01: Tests returning details for the only user in the server 
def test_user_all01():
    test_user = create_user()
    users_dictionary = {
        'users' : [
            profile(test_user['token'],['u_id'])['user']
        ]
    }
    assert all_(test_user['token']) == users_dictionary


#test_user_all02: Test returning > 1 users in a server
def test_user_all02():
    user1 = auth.register("Test@test.com", "test", "John", "Smith")
    user2 = auth.register("NotExample@example.com", "Example", "John", "Smith")
    user3 = auth.register("InvalidExample@example.com", "Example", "John", "Smith")
    
    users_dictionary = {
        'users' : [
            profile(user1['token'],user1['u_id'])['user'],
            profile(user2['token'],user2['u_id'])['user'],
            profile(user3['token'],user3['u_id'])['user']
        ]
    }
    assert all_(user2['token']) == users_dictionary


#test_user_all03: Test multiple people using the users.user all. All users 
#should get the same result
def test_user_all03():
    user1 = auth.register("Test@test.com", "test", "John", "Smith")
    user2 = auth.register("NotExample@example.com", "Example", "John", "Smith")
    user3 = auth.register("Invample@example.com", "Example", "John", "Smith")
    
    users_dictionary = {
        'users' : [
            profile(user1['token'],user1['u_id'])['user'],
            profile(user2['token'],user2['u_id'])['user'],
            profile(user3['token'],user3['u_id'])['user']
        ]
    }
    
    assert all_(user1['token']) == users_dictionary
    assert all_(user2['token']) == users_dictionary
    assert all_(user3['token']) == users_dictionary


#test_user_all04: Test that a user in a channel can still user user_all function
#and gets all users within the server. Similarly, people outside the channel will
#get all users including ones in the channel.
def test_user_all04():
    user1 = auth.register("Test@test.com", "test", "John", "Smith")
    user2 = auth.register("NotExample@example.com", "Example", "Jhn", "Smith")
    user3 = auth.register("Invample@example.com", "Example", "Jon", "Smith")
    user4 = auth.register("tsa@test.com", "Example", "Bon", "Smoth")
    
    pub_channel = channels.create(user1['token'], 'awesomechannel', True)
    priv_channel = channels.create(user2['token'], 'notcool', False)
    
    channel.joi(user3['token'],pub_channel['channel_id'])
    channel.joi(user2['token'],priv_channel['channel_id'])

    users_dictionary = {
        'users' : [
            profile(user1['token'],user1['u_id']),
            profile(user2['token'],user2['u_id']),
            profile(user3['token'],user3['u_id']),
            profile(user4['token'],user4['u_id'])
        ]
    }
    
    assert all_(user1['token']) == users_dictionary
    assert all_(user2['token']) == users_dictionary
    assert all_(user3['token']) == users_dictionary
    assert all_(user4['token']) == users_dictionary
