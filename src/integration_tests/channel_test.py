import app.channel as ch
import app.channels as chs
import pytest as pt
from main.error import InputError, AccessError
from app.auth import login, logout, register
from app.message import send


########################
# Helper Functions
#######################

# Send a few messages to a given channel and return list of message_ids
def _send_messages(details, ch_id, n):
    msg_ids = []

    response = send(details["token"], ch_id, "First message")
    msg_ids.append(response["message_id"])

    for i in range(1, n):
        msg_ids.append(send(details["token"], ch_id,
                            f"another message {i}")["message_id"])

    return msg_ids


# Make sure member id's are legit
def assert_u_id(member):
    assert isinstance(member['u_id'], int) and len(member['u_id']) <= 16


# Make sure u_ids are unique in a channel listing
def conflict_id(member_list):
    conflicting = []
    for member in member_list:
        if member_list.count(member) > 1:
            conflicting.append(member["u_id"])

    return len(conflicting) > 0


# Ensure that certain users are not owners or certain members not in channel
def _members_not_owners(owners, user_id):
    for X in owners:
        if user_id == X["u_id"]:
            return False

    return True


# Return fixture class instances, if run into errors with direct class passing
@pt.fixture(scope="module")
def validUser():
    return _validUser()


@pt.fixture(scope="module")
def owner():
    return _owner()


#####################
# CLASSES
####################


# A standard user(s).
class _validUser:
    details = register("validemail@gmail.com",
                       "GoodPassword", "Plebian", "Person")

    details2 = register("veryvalidemail@gmail.com",
                        "veryGoodPassword", "Noble", "Person")

    details_part_owner = register(
        "Are_ya_coding_son@gmail.com", "very_partially_owner", "Yes", "WhyWouldntIbe")


# An owner of a channel
class _owner(_validUser):

    # Register an owner
    details = register("Owner_111@gmail.com",
                       "AmazingPassword", "Hyper", "Swine")

    # Create a public channel
    real_channel = chs.create(
        details["token"], "CNN_aka_fake_news", True)

    # Create a private channel
    priv_channel = chs.create(
        details["token"], "Nine_News", False)

    # Send some messages
    msgs_ids = _send_messages(details, real_channel["channel_id"], 10)

    # Dictionary of all channels
    all_channels = chs.listall(details["token"])

    # Dictionary of channels you belong to
    some_channels = chs.list_(details["token"])

    # Dictionary of channel members
    ch_members = ch.det(
        details["token"], real_channel["channel_id"])

    # Add user as member
    ch.inv(details["token"], real_channel["channel_id"],
           _validUser.details_part_owner["u_id"])

    # Add another user as owner
    ch.add_owner(details["token"], real_channel["channel_id"],
                 _validUser.details_part_owner["u_id"])


####################
# TESTS
###################


# TESTS for inv() when the owner and channel members invite.


# Basic tests to ensure function returns an empty dictionary on valid input.
def test_chnv00(validUser, owner):

    # Slack owner invites
    assert ch.inv(
        owner.details["token"], owner.real_channel["channel_id"], validUser.details["u_id"]) == {}

    ch.lev(validUser.details["token"], owner.real_channel["channel_id"])

    # When a standard owner invites
    assert ch.inv(validUser.details_part_owner["token"],
           owner.real_channel["channel_id"], validUser.details["u_id"]) == {}

    ch.lev(validUser.details["token"], owner.real_channel["channel_id"])


# Is channel_id valid?
def test_chnv01(validUser, owner):

    with pt.raises(InputError) as e:
        ch.inv(
            owner.details["token"], 'INVALID_CHANNEL_ID', validUser.details["u_id"])
        print(f"As Expected {e}: Channel ID is invalid")


# Secondary tests for valid input.
def test_chnv02(validUser, owner):

    # Is user_id in valid format?
    with pt.raises(InputError) as e:
        ch.inv(
            owner.details["token"], owner.real_channel["channel_id"], "NOT_VALID_ID")
        print(f"As Expected {e}: User ID is invalid")

    with pt.raises(InputError) as f:
        # assuming user_id isnt longer than 12 digits
        ch.inv(
            owner.details["token"], owner.real_channel["channel_id"], 1215279129507125)
        print(f"As Expected {f}: User ID is longer than 12 digits")

    with pt.raises(InputError) as g:
        # Does the function catch a float?
        ch.inv(owner.details["token"],
               owner.real_channel["channel_id"], 42068.5)
        print(
            f"As Expected {g}: User ID cannot be represented as a floating point value")


# Is the 'authorized user' already a member of the channel?
def test_chnv04(validUser, owner):

    # Need to confirm that user is not in channel => make a secondary user with details2
    assert validUser.details2["u_id"] not in owner.ch_members["all_members"]
    with pt.raises(AccessError) as e:
        ch.inv(
            validUser.details2["token"], owner.real_channel["channel_id"], validUser.details["u_id"])
        print(
            f"As Expected {e}: A non-member cannot invite another non-member")

    with pt.raises(AccessError) as e:
        ch.inv(
            validUser.details2["token"], owner.real_channel["channel_id"], validUser.details2["u_id"])
        print(
            f"As Expected {e}: A non-member cannot invite the owner to his own channel")


# Is the token valid?
def test_chnv05(validUser, owner):

    # Check a non-existent token
    with pt.raises(AccessError) as e:
        ch.inv(
            "INVALID_TOKEN", owner.real_channel["channel_id"], validUser.details["u_id"])
        print(f"As Expected {e}: Invalid Token")

    # Is the token in a valid format?
    with pt.raises(AccessError) as f:
        ch.inv(
            215125809, owner.real_channel["channel_id"], validUser.details["u_id"])
        print(f"As Expected {f}: Invalid format, int for token")


# TESTS FOR det()...


# Basic test to confirm valid return value
def test_chde00(validUser, owner):

    # Ensure that we have no conflicting u_ids
    assert conflict_id(owner.ch_members["all_members"]) == False
    assert ch.det(owner.details["token"], owner.real_channel["channel_id"])


# Is channel_id valid?
def test_chde01(validUser, owner):
    with pt.raises(InputError):
        ch.det(owner.details["token"], "INVALID_CHANNEL_ID")


# Is user even a member of the channel?
def test_chde02(validUser, owner):
    with pt.raises(AccessError):
        ch.det(
            validUser.details2["token"], owner.real_channel["channel_id"])


# Is the ch_id in a valid format? (These types of tests are more useful later on)
def test_chde03(validUser, owner):
    ch1 = ch.det(
        owner.details["token"], owner.real_channel["channel_id"])
    assert isinstance(ch1["name"], str)


# Are the user_ids of the owners and members valid?
def test_chde04(validUser, owner):

    # Retrieve channel details manually
    ch1 = ch.det(
        owner.details["token"], owner.real_channel["channel_id"])

    # Assert u_ids are integers
    map(lambda owner: assert_u_id(owner), ch1["owner_members"])
    map(lambda members: assert_u_id(members), ch1["all_members"])


# TESTS for msg


# Basic tests
def test_chmsg00(validUser, owner):

    # Retrieve messages 0 up to 50.
    messages = ch.msg(owner.details["token"], owner.real_channel["channel_id"], 0)[
        "messages"]

    # Have to do it this way since we do not know timestamp
    assert messages[0]["u_id"] == owner.details["u_id"] and\
    messages[9]["message"] == "First message"


# Test for valid ch_id
def test_chmsg01(validUser, owner):
    with pt.raises(InputError):
        ch.msg(owner.details["token"], "INVALID_CHANNEL_ID", 0)


# Test for 'start' <= number of messages in the channel
def test_chmsg02(validUser, owner):
    ch_msgs = ch.msg(
        owner.details["token"], owner.real_channel["channel_id"], 0)

    assert ch_msgs["start"] <= len(ch_msgs["messages"])


# Test for valid member of channel
def test_chmsg03(validUser, owner):
    with pt.raises(AccessError):
        ch.msg(
            validUser.details2["token"], owner.real_channel["channel_id"], 0)


# TESTS for lev


# Basic test
def test_chlv00(validUser, owner):

    # Assume validUser1 not in channel yet
    ch.inv(
        owner.details["token"], owner.real_channel["channel_id"], validUser.details["u_id"])
    assert ch.lev(validUser.details["token"], owner.real_channel["channel_id"]) == {}


# Is valid channel_id?
def test_chlv01(validUser, owner):
    with pt.raises(InputError):
        ch.lev(owner.details["token"], "INVALID_CHANNEL_ID")


# Test for valid member of channel
def test_chlv02(validUser, owner):

    # User not part of channel
    with pt.raises(AccessError):
        ch.lev(
            validUser.details2["token"], owner.real_channel["channel_id"])
    # Token is invalid
    with pt.raises(AccessError):
        ch.lev("INVALID_TOKEN", owner.real_channel["channel_id"])


# TESTS for joi


# Basic test
def test_chjn00(validUser, owner):
    assert ch.joi(
        validUser.details["token"], owner.real_channel["channel_id"]) == {}

    ch.lev(validUser.details["token"], owner.real_channel["channel_id"])


# Is valid channel_id?
def test_chjn01(validUser, owner):
    with pt.raises(InputError):
        ch.joi(owner.details["token"], "INVALID_CHANNEL_ID")


# Is the channel private? Does the user have super_user (admin) rights to join?
def test_chjn02(validUser, owner):

    # Non-member attempting to join a private channel
    with pt.raises(AccessError):
        ch.joi(validUser.details2["token"], owner.priv_channel["channel_id"])


# TESTS for add_owner


# Basic test
def test_chadd00(validUser, owner):
    assert validUser.details2["u_id"] not in owner.ch_members["all_members"]
    ch.inv(owner.details["token"], owner.real_channel["channel_id"], validUser.details2["u_id"])
    assert ch.add_owner(
        owner.details["token"], owner.real_channel["channel_id"], validUser.details2["u_id"]) == {}


# Is valid channel_id?
def test_chadd01(validUser, owner):
    with pt.raises(InputError):
        ch.add_owner(
            owner.details["token"], "INVALID_CHANNEL_ID", validUser.details2["u_id"])


# Is user already an owner?
def test_chadd02(validUser, owner):

    # For the slack owner
    with pt.raises(InputError):
        ch.add_owner(
            owner.details["token"], owner.real_channel["channel_id"], owner.details["u_id"])

    # For secondary owners
    with pt.raises(InputError):
        ch.add_owner(
            owner.details["token"], owner.real_channel["channel_id"], validUser.details2["u_id"])

# Is the person being added a member?
def test_chadd03(validUser, owner):
    with pt.raises(InputError):
        ch.add_owner(
            owner.details["token"], owner.real_channel["channel_id"], validUser.details2["u_id"])


# TESTS for rem_owner

# Basic test
def test_chrm00(validUser, owner):
    assert ch.rem_owner(
        owner.details["token"], owner.real_channel["channel_id"], validUser.details2["u_id"]) == {}


# Is valid channel_id?
def test_chrm01(validUser, owner):
    with pt.raises(InputError):
        ch.rem_owner(owner.details["token"],
                     "INVALID_CHANNEL_ID", owner.details["u_id"])


# Is the user being removed even an owner?
def testchrm02(validUser, owner):
    if _members_not_owners(owner.ch_members["owner_members"], validUser.details["u_id"]):
        with pt.raises(InputError):
            ch.rem_owner(
            owner.details["token"], owner.real_channel["channel_id"], validUser.details["u_id"])

    with pt.raises(InputError):
        ch.rem_owner(
            owner.details["token"], owner.real_channel["channel_id"], validUser.details["u_id"])


# Is remover an owner of slackr or the channel's owner?
def test_chrm03(validUser, owner):
    with pt.raises(InputError):
        ch.rem_owner(
            validUser.details["token"], owner.real_channel["channel_id"], validUser.details["u_id"])


# Is the person being removed the slack's owner?
def test_chrm04(validUser, owner):
    assert ch.rem_owner(validUser.details_part_owner["token"],
                     owner.real_channel["channel_id"], owner.details["u_id"]) == {}
