import pytest
from app.auth import register
from app.channels import create
from app.message import edit, remove, send
from app.channel import joi, lev
from main.error import InputError, AccessError
from app.workspace import workspace_reset
# All tests assume that auth_ and channel_ and channels_ functions are functioning fully.

# Create dummy user and channel
# Sometimes, we need to create more than one user and/or channel. For this, we pass
# id 2 instead of id 1 which creates a distinct user and channel and returns it.
# The return value is a tuple.
# tuple[0] is the dictionary for the newly created user, {'token': (token), 'u_id': (u_id)}
# tuple[1] is the newly created channel ID.
def create_data(id):
    workspace_reset()
    if id == 1:
        testUser = register("test@test.com", "password123", "Test", "User")
        testChannel = create(testUser['token'], "testChannel", True)
        return (testUser, testChannel)
    elif id == 2:
        testUser = register("test2@test.com", "password123", "Test2", "User2")
        testChannel = create(testUser['token'], "testChannel2", True)
        return (testUser, testChannel)

####################
#### SEND TESTS ####
####################

# Test a standard message
def test_send_basic():
    testData = create_data(1)
    result = send(testData[0]['token'], testData[1]['channel_id'], "very legal and very cool")


# Test with an assumed invalid token
# See assumptions
def test_send_invalid_token():
    testData = create_data(1)
    with pytest.raises(AccessError):
        send("NOT_VALID_TOKEN", testData[1]['channel_id'], "The Middle East is complicated business")

# Test with an assumed invalid channel ID
# See assumptions
def test_send_invalid_channel_id():
    testData = create_data(1)
    with pytest.raises(AccessError):
        send(testData[0]['token'], -1, "aaa")

# Send with a message that is too long
def test_send_createlong():
    testData = create_data(1)

    #Create 1001 character message
    longString = "x" * 1001
    with pytest.raises(InputError):
        send(testData[0]['token'], testData[1]['channel_id'], longString)

# Send with a message that is just short enough
def test_send_createjust_short():
    testData = create_data(1)

    #Create 1000 character message
    shortString = "x" * 1000
    result = send(testData[0]['token'], testData[1]['channel_id'], shortString)


# Test with an empty message
# See assumptions
def test_send_createempty():
    testData = create_data(1)

    #Create 1001 character message
    with pytest.raises(InputError):
        send(testData[0]['token'], testData[1]['channel_id'], "")

# Test where a user has not yet joied the channel
def test_send_not_jonied():
    testData = create_data(1)
    lev(testData[0]['token'], testData[1]['channel_id'])
    with pytest.raises(AccessError):
        send(testData[0]['token'], testData[1]['channel_id'], "The mainstream media!")

######################
#### REMOVE TESTS ####
######################

# Test with an assumed invalid token
# See assumptions
def test_remove_invalid_token():
    testData = create_data(1)
  
    testMessage = send(testData[0]['token'], testData[1]['channel_id'], "Message")['message_id']
    testData[0]['token'] = "NOT_VALID_TOKEN"
    with pytest.raises(AccessError):
        remove("NOT_VALID_TOKEN", testMessage)

# Test where message cannot be found (e.g. has been removed)
def test_remove_createnot_found():
    testData = create_data(1)

    with pytest.raises(InputError):
        remove(testData[0]['token'], 000000000000)

# Test remove is allowed through where user is not authorised but is admin
def test_remove_unauthorised_admin():
    # Create 1 admin of channel and 1 member of channel
    testData = create_data(1)
    testData2 = create_data(2)
    # The user of testData is owner (joied first - see assumptions)

    joi(testData2[0]['token'], testData[1]['channel_id'])
    testMessage = send(testData2[0]['token'], testData[1]['channel_id'], "Test")

    # The user of testData2 sent the message but testData is the owner/admin of †he channel so should be able to remove
    result = remove(testData[0]['token'], testMessage)
    assert type(result) is dict
    assert result == {}

# Test remove is allowed through where user is authorised but is not admin
def test_remove_authorised_not_admin():
    testData = create_data(1)
    testData2 = create_data(2)

    joi(testData2[0]['token'], testData[1]['channel_id'])

    # The user of testData2 sent the message; but is not an admin (did not joi the channel first - see assumptions)
    testMessage = send(testData2[0]['token'], testData[1]['channel_id'], "Message")

    # The user of testData2 should still be able to remove the message
    result = remove(testData2[0]['token'], testMessage)
    assert type(result) is dict
    assert result == {}

# Test remove does NOT go through where user meets neither of the aforementioned conditions 
def test_remove_unauthorised_not_admin():
    testData = create_data(1)
    testData2 = create_data(2)

    joi(testData2[0]['token'], testData[1]['channel_id'])
    # testData sent the message and is admin
    testMessage = send(testData2[0]['token'], testData[1]['channel_id'], "Message")
    # testData sent the message and testData is the owner/admin of BOTH the slackr and the channel so testData 2 shouldn't be able to remove
    with pytest.raises(AccessError):
        remove(testData2[0]['token'], testMessage)


####################
#### EDIT TESTS ####
####################

# Test where message cannot be found (e.g. has been removed)
# See assumptions


# Test with an assumed invalid token
def test_edit_invalid_token():
    testData = create_data(1)
  
    testMessage = send(testData[0]['token'], testData[1]['channel_id'], "Message")
    with pytest.raises(AccessError):
        edit("NOT_VALID_TOKEN", testMessage, "new message")

def test_edit_createnot_found():
    testData = create_data(1)

    with pytest.raises(InputError):
        edit(testData[0]['token'], 000000000000, "We should have gotten more of the oil in Syria")

# Test edit goes through where user is not authorised but is admin
def test_edit_unauthorised_admin():
    #C reate 1 admin of channel and 1 member of channel
    testData = create_data(1)
    testData2 = create_data(2)
    # The user of testData is owner

    joi(testData2[0]['token'], testData[1]['channel_id'])
    testMessage = send(testData2[0]['token'], testData[1]['channel_id'], "Test")

    # The user of testData2 sent the message but testData is the owner/admin so should be able to edit
    result = edit(testData[0]['token'], testMessage, "newmessage")
    assert type(result) is dict
    assert result == {}

# Test edit goes through where user is authorised and is not admin
def test_edit_authorised_not_admin():
    testData = create_data(1)
    testData2 = create_data(2)

    joi(testData2[0]['token'], testData[1]['channel_id'])

    # The user of testData2 sent the message; but is not an admin
    testMessage = send(testData2[0]['token'], testData[1]['channel_id'], "Message")

    # The user of testData2 should still be able to edit the message
    result = edit(testData2[0]['token'], testMessage, "new msg")
    assert type(result) is dict
    assert result == {}

# Test edit does NOT go through where user meets neither of the aforementioned condition 
def test_edit_unauthorised_not_admin():
    testData = create_data(1)
    testData2 = create_data(2)

    joi(testData2[0]['token'], testData[1]['channel_id'])
    
    # The user of testData sent the message and is admin
    testMessage = send(testData2[0]['token'], testData[1]['channel_id'], "Message")
    # The user of testData sent the message and testData is the owner/admin so testData 2 shouldn't be able to remove
    with pytest.raises(AccessError):
        edit(testData2[0]['token'], testMessage, "newMessage")
    
# Test that if the new string is an empty stirng, the message is deleted.
def test_edit_empty_string():
    testData = create_data(1)

    testMessage = send(testData[0]['token'], testData[1]['channel_id'], "This is a message that should be removed")
    result = edit(testData[0]['token'], testMessage, "") # Should NOT throw an error here - should remove the message

    # First, a quick sanity check on the return value and type
    assert type(result) is dict
    assert result == {}

    # Now, we can check the message is actually gone by trying to remove it (should throw AccessError - should have been deleted)
    with pytest.raises(InputError):
        remove(testData[0]['token'], testMessage)
