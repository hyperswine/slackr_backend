import pytest
from app.auth import register
from app.channel import joi, lev
from app.channels import create, list_, listall
from app.workspace import workspace_reset
from main.error import InputError, AccessError

# All tests assume that auth_ and channel_ functions are functioning fully.

# Create dummy user and return
@pytest.fixture
def create_user():
    workspace_reset()
    return register("test@test.com", "password123", "Test", "User")

######################
#### CREATE TESTS ####
######################

def test_create_basic(create_user):
    result = create(create_user['token'], "My Channel", True)
    assert type(result) is dict
    assert type(result['channel_id']) is int

# Check that everything works well when the channel is not public
def test_create_private(create_user):
    result = create(create_user['token'], "My Channel", False)
    assert type(result) is dict
    assert type(result['channel_id']) is int

# Test that when name is too long an InputError is thrown
def test_create_name_long(create_user):
    longString = "x" * 21
    with pytest.raises(InputError):
        create(create_user['token'], longString, True)

# Test that when is just short enough everything works
def test_create_name_just_short(create_user):
    shortString = "x" * 20
    result = create(create_user['token'], shortString, True)
    assert type(result) is dict
    assert type(result['channel_id']) is int

# Test with an assumed invalid token - see assumptions
def test_create_invalid_token(create_user):
    with pytest.raises(AccessError):
        create("NOT_VALID_TOKEN", "Test ", True)

# Test with an empty name - see assumptions
def test_create_empty_name(create_user):
    with pytest.raises(InputError):
        create(create_user['token'], "", True)


####################    
#### LIST TESTS ####
####################

# Test where authorised user is not part of any channels
# Assumes that _create is working correctly.

def test_list_no_channels(create_user):  
    assert list_(create_user['token']) == {'channels': []}
    
def test_list_in_single_channel(create_user): 
    testChannel = create(create_user['token'], "My Channel", True)
    assert list_(create_user['token']) == {'channels': [{'channel_id': testChannel['channel_id'], 'name': 'My Channel'}]}

def test_list_in_single_private_channel(create_user): 
    testChannel = create(create_user['token'], "My Channel", False)
    assert list_(create_user['token']) == {'channels': [{'channel_id': testChannel['channel_id'], 'name': 'My Channel'}]}

def test_list_in_two_channel(create_user):
    testChannel = create(create_user['token'], "My Channel", True)
    testChannel2 = create(create_user['token'], "My Channel2", True)
    
    assert list_(create_user['token']) == {'channels': 
                                                    [{
                                                        'channel_id': testChannel['channel_id'], 
                                                        'name': 'My Channel'
                                                    }, 
                                                    {
                                                        'channel_id': testChannel2['channel_id'], 
                                                        'name': 'My Channel2'
                                                    }]
                                                }   


def test_list_in_absent_in_channel(create_user):
    
    testChannel = create(create_user['token'], "My Channel", True)
    id = create(create_user['token'], "My Channel2", True)['channel_id']
    lev(create_user['token'], id)
    assert list_(create_user['token']) == {'channels': [{'channel_id': testChannel['channel_id'], 'name': 'My Channel'}]} 


def test_list_in_absent_in_multiple_channels(create_user):
    
    id1 = create(create_user['token'], "My Channel", True)['channel_id']
    id2 = create(create_user['token'], "My Channel2", True)['channel_id']
    lev(create_user['token'], id1)
    lev(create_user['token'], id2)

    assert list_(create_user['token']) == {'channels': []}

# Test with an assumed invalid token - see assumption
def test_list_invalid_token():
    with pytest.raises(AccessError):
        list_("NOT_VALID_TOKEN")

#######################
#### listall TESTS ####
#######################

def test_listall_no_channels(create_user):
    assert listall(create_user['token']) == {'channels': []}

def test_listall_in_single_channel(create_user): 
    testChannel = create(create_user['token'], "My Channel", True)
    assert listall(create_user['token']) == {'channels': [{'channel_id': testChannel['channel_id'], 'name': 'My Channel'}]}

def test_listall_in_single_private_channel(create_user): 
    testChannel = create(create_user['token'], "My Channel", False)
    assert listall(create_user['token']) == {'channels': []}

def test_listall_in_two_channel(create_user):
    testChannel = create(create_user['token'], "My Channel", True)
    testChannel2 = create(create_user['token'], "My Channel2", True)
    
    assert listall(create_user['token']) == {'channels': 
                                                    [{
                                                        'channel_id': testChannel['channel_id'], 
                                                        'name': 'My Channel'
                                                    }, 
                                                    {
                                                        'channel_id': testChannel2['channel_id'], 
                                                        'name': 'My Channel2'
                                                    }]
                                                }   


def test_listall_in_absent_in_channel(create_user):
    
    testChannel = create(create_user['token'], "My Channel", True)
    testChannel2 = create(create_user['token'], "My Channel2", True)
    lev(create_user['token'], testChannel['channel_id'])
    assert listall(create_user['token']) == {'channels': 
                                                    [{
                                                        'channel_id': testChannel['channel_id'], 
                                                        'name': 'My Channel'
                                                    },
                                                    {
                                                        'channel_id': testChannel2['channel_id'],
                                                        'name': 'My Channel2'
                                                    }]
                                                }  

def test_listall_in_absent_in_multiple_channels(create_user):
    
    testChannel = create(create_user['token'], "My Channel", True)
    testChannel2 = create(create_user['token'], "My Channel2", True)
    testChannel3 = create(create_user['token'], "My Channel3", True)

    assert listall(create_user['token']) == {'channels': 
                                                    [{
                                                        'channel_id': testChannel['channel_id'], 
                                                        'name': 'My Channel'
                                                    }, 
                                                    {
                                                        'channel_id': testChannel2['channel_id'], 
                                                        'name': 'My Channel2'
                                                    },
                                                    {
                                                        'channel_id': testChannel3['channel_id'], 
                                                        'name': 'My Channel3'
                                                    }]
                                                }   

# Test with an assumed invalid token - see assumption
def test_listall_invalid_token():
    with pytest.raises(AccessError):
        listall("NOT_VALID_TOKEN")
