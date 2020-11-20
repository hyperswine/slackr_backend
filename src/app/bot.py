'''
This module stores a general purpose 'bot'
for the entire slackr.

Usages - For rendering hangman or sending errors into
the chat in each channel.
'''
from main.data import user_data, all_channels
import aux_.common as common
import aux_.discrete as discrete
from app.channel import joi
from app.auth import register, login
import app.message as message

# This is what the data for the bot could look like.
bot_data = {
    'u_id': 420420420,
    'email': "totallynotrobot@human.com",
    'first_name': "Iam",
    'last_name': "Robot",
    'handle': "BOT1",
    'password': "1010101000101010",
    'is_owner_of_slackr': True,
    'is_logged_in': True,
    'reset_code': 1337420,
    'profile_img_url': 'http://127.0.0.1:8080/profileimages/default.jpg'
}


def auto_register():
    '''
    Once called, registers the bot to the slackr.
    '''
    global user_data
    # check if bot has already been registered
    bot_id = discrete.find_uid("totallynotrobot@human.com")
    if bot_id != -1:
        print("Bot has already been registered")
        if not user_data[bot_id]["is_logged_in"]:
            login("totallynotrobot@human.com", "1010101000101010")
        return

    # register the bot
    register(bot_data["email"], bot_data["password"],
             bot_data["first_name"], bot_data["last_name"])

    user_data[bot_id]["profile_img_url"] = "http://127.0.0.1:8080/profileimages/bot.jpg"


def bot_send(messageX, channel_id):
    '''
    Input - message < 1000 length, and valid channel_id.

    Sends a message with the bot to a channel.
    '''
    # register and join the channel if haven't already
    auto_register()
    bot_id = discrete.find_uid("totallynotrobot@human.com")
    for channel in all_channels:
        if channel["channel_id"] == channel_id:
            if bot_id not in channel["all_members"]:
                bot_join(channel_id)

    # send the message
    token_bot = common.encode_token({"u_id": bot_id})
    message.send(token_bot, channel_id, messageX)


def bot_join(channel_id):
    '''
    Input - channel_id

    Joins a channel directly as a bot.
    No message is shown upon joining.
    '''
    # join a channel as a bot.
    # NOTE: cannot join private channels.
    for channel in all_channels:
        if channel["channel_id"] == channel_id:
            bot_id = discrete.find_uid("totallynotrobot@human.com")
            token_bot = common.encode_token({"u_id": bot_id})
            joi(token_bot, channel_id)
