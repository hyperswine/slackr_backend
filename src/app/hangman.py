'''
This module stores all the methods pertaining to hangman.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from main.data import hangman_sessions, message_data, next_id, user_data
from main.error import InputError, AccessError
from app.bot import bot_send, bot_data, bot_join
import aux_.common as common
import aux_.discrete as discrete
import app.message as message
import random
import re
import requests

_hangman = [
    "~~~ no wrong guesses yet ヽ(•‿•)ノ ~~~",
    """
    |====
    |
    |
    |
    |
    |
    -------
    """,
    """
    |====
    |   |
    |
    |
    |
    |
    -------
    """,
    """
    |====
    |   |
    |  O
    |
    |
    |
    -------
    """,
    """
    |====
    |   |
    |  O
    |   |
    |
    |
    -------
    """,
    """
    |====
    |   |
    |  O
    |  /|
    |
    |
    -------
    """,
    """
    |====
    |   |
    |  O
    |  /|\\
    |
    |
    -------
    """,
    """
    |====
    |   |
    |   O
    |  /|\\
    |  /
    |
    -------
    """,
    """
    |====
    |   |
    |  O
    |  /|\\
    |  / \\
    |
    -------
    """,
]


def start(token, channel_id, word):
    '''
    Input - valid token, channel_id and word.

    Word validity is handled in the frontend.

    Behavior:

    Starts a hangman session in a channel.
    Takes a word from the random_word mod, and parses
    it so that it only contains alphabetical characters.

    All hangman sessions are stored in a hangman data structure.

    Output - {}
    '''
    # ch_id is invalid -> InputError
    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(
            description='The channel you are attempting to start a hangman in does not exist.')

    # check if token is valid
    authorized_caller = common.decode_token(token)
    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            description='You do not have permission to start hangman.')

    # check if a hangman session is ongoing
    for session in hangman_sessions:
        if session["channel_id"] == channel_id:
            raise InputError(
                description='A hangman session is already ongoing in this channel')

    final_word = word[0].split(' ')

    # if word not specified (is list), generate a random word
    if len(final_word) == 1:
        _site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = requests.get(_site)
        _words = response.content.splitlines()
        final_word = random.choice(_words).decode()
    else:
        final_word = final_word[1].strip()
    # add to hangman sessions
    hangman_sessions.append({
        "channel_id": channel_id,
        "word": final_word.lower(),
        "decrement_word": final_word.lower(),
        "guesses": [],
        "remaining_guesses": 8,
        "bad_attempts": 0
    })

    # send message as the bot
    idX = discrete.find_user(authorized_caller["u_id"])
    starter_name = user_data[idX]["first_name"]
    bot_message = f"{starter_name} has just started a hangman!"
    bot_message += _missing([], final_word)
    bot_send(bot_message, channel_id)

    return {}


def guess(token, channel_id, X):
    '''
    Input - valid token, channel ID and a guess X.

    Behavior:
    Given a message with some 2nd string 'X', determines
    whether the guess is correct or not.

    Output - {}
    '''
    # ch_id is invalid -> InputError

    index = common.ch_id_exists(channel_id)
    if index == -1:
        raise InputError(
            description='The channel you are guessing on does not exist.')

    # check if token is valid
    authorized_caller = common.decode_token(token)
    if authorized_caller == {"u_id": "error_invalid_token"} or \
            not common.user_in_channel(authorized_caller["u_id"], channel_id):
        raise AccessError(
            description='You do not have permission to do this.')
    # ensure channel has a hangman session
    # NOTE YOU must abstract these functions ASAP.
    index = None
    for session in hangman_sessions:
        if session["channel_id"] == channel_id:
            index = hangman_sessions.index(session)
    if index == None:
        raise InputError(description='A hangman session is not running right now')

    X = X[0].split(' ')

    # if word not specified (is list), generate a random word
    if len(X) != 1:
        X = X[1]

    # check if X has been guessed already
    if X in hangman_sessions[index]['guesses']:
        raise InputError(description='Your guess has already been guessed.')

    # catch empty input error
    if not isinstance(X, str):
        raise InputError(description='Usage: /guess [letter]')
    # SEND THE /guess X as a message to message data.
    message.send(token, channel_id, '/guess ' + X)

    # check if the guess results in the complete answer
    hm_word = hangman_sessions[index]['word']
    guesses = hangman_sessions[index]['guesses']
    guesses.append(X)
    prev_word = hangman_sessions[index]['decrement_word']
    hangman_sessions[index]['decrement_word'] = hangman_sessions[index]['decrement_word'].replace(X, '')
    word_decrement = hangman_sessions[index]['decrement_word']
    if prev_word == word_decrement:
        hangman_sessions[index]["bad_attempts"] += 1

    # render ASCII or some image art.
    bot_message = _render_ascii(
        hangman_sessions[index]["bad_attempts"], channel_id, guesses, hm_word)

    if hm_word.replace(X, '') == hm_word:
        hangman_sessions[index]['remaining_guesses'] -= 1

    # if guess results in complete answer, then done and send congratulations
    if word_decrement == '':
        hangman_sessions.pop(index)
        bot_message += "\n＼(＾O＾)／\nYou've correctly guessed the word!"
    # decrement the amount of guesses available, and if no more guesses,
    # remove hangman session and send taunting message
    else:
        if hangman_sessions[index]['remaining_guesses'] == 0:
            hangman_sessions.pop(index)
            bot_message += f"\n(✖╭╮✖)\nThe word is {hm_word}, you have lost\nF to pay respects"
        else:
            bot_message += "\nLetters guessed:"
            for word in hangman_sessions[index]['guesses']:
                bot_message += f" {word}"
    # send message as the bot
    bot_send(bot_message, channel_id)

    return {}


def _render_ascii(n, channel_id, guessed, word):
    '''
    Input - number of bad attempts and misc.

    Renders an ascii art of hangman based on how many failed
    attempts.

    Output - pure art.
    '''
    # Sends the art to a bot on a 1 sec delay
    ART = _hangman[n] + _missing(guessed, word)
    return ART


def _missing(guessed, word):
    '''
    Input - word, guessed subwords.

    Fill in the blanks.

    Output - Word progress bar.
    '''
    # create a ____ word
    total_word = '\n' + word

    # for each letter in word that isnt in dec_word
    # replace index total_word[i] with word[i]
    for x in word:
        if x not in guessed:
            total_word = total_word.replace(x, ' _ ')

    return total_word
