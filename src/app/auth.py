
'''
This module stores all the backend functions for the '/auth' route.
Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from admin.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from main.error import InputError
from main.data import user_data, next_id
import aux_.common as aux_common
import aux_.discrete as aux_discrete


def register(email, password, name_first, name_last):
    '''
    ## DESCRIPTION ##
    Given a email, password, name_first and name_last, create a new account for
    them and return a new token for authentication in their session. A handle is
    generated that is the concatentation of a lowercase-only first name and last
    name. If the concatenation is longer than 20 characters, it is cutoff at 20
    characters. If the handle is already taken, you may modify the handle in any
    way you see fit to make it unique.

    ## TYPES ##
    email - string
    password - string
    name_first - string
    name_last - string

    ## RETURN VALUE ##
    {u_id, token}

    ## EXCEPTIONS ##
    InputError if
        - Invalid email
        - Email is already being used
        - Password is less than 6 characters long
        - name_first not is between 1 and 50 characters inclusive in length
        - name_last not is between 1 and 50 characters inclusive in length
    '''

    global user_data, next_id

    if len(password) <= 5:
        raise InputError(
            description="Password entered is less than 6 characters long")

    if len(name_first) <= 0 or len(name_first) > 50:
        raise InputError(
            description="First name must be between 1 and 50 characters long.")

    if len(name_last) <= 0 or len(name_last) > 50:
        raise InputError(
            description="Last name must be between 1 and 50 characters long.")

    if not aux_discrete.check_email_valid(email):
        raise InputError(description="Email entered is not a valid email")

    if not aux_discrete.check_email_in_use(email):
        raise InputError(
            description="Email address is already being used by another user")

    next_u_id = next_id.get('u_id')
    if not next_u_id: # key does not exist yet
        next_id['u_id'] = 0
        next_u_id = 0

    next_id['u_id'] += 1

    new_user_dict = {
        "u_id": next_u_id,
        "email": email,
        "first_name": name_first,
        "last_name": name_last,
        "password": password,
        "handle": aux_discrete.new_handle(name_first, name_last),
        "is_owner_of_slackr": True if len(user_data) == 0 else False,
        "is_logged_in": True,
        "profile_img_url": "http://127.0.0.1:8080/profileimages/default.jpg"
    }

    user_data.append(new_user_dict)

    return {'u_id': next_u_id, 'token': aux_common.encode_token({'u_id': next_u_id})}


def login(email, password):
    '''
    ## DESCRIPTION ##
    Given a registered users' email and password and generates a valid token for
    the user to remain authenticated

    ## TYPES ##
    email - string
    password - string

    ## RETURN VALUE ##
    {u_id, token}

    ## EXCEPTIONS ##
    InputError if
        - Invalid email
        - Email entered does not belong to a user
        - Incorrect password
    '''

    global user_data

    registered_email = False

    if not aux_discrete.check_email_valid(email):
        raise InputError(description="Email entered is not a valid email")

    for user in user_data:
        if user["email"] == email:
            registered_email = True

    if not registered_email:
        raise InputError(description="Email entered does not belong to a user")

    for user in user_data:
        if user["email"] == email and user["password"] != password:
            raise InputError(description="Password is not correct")

    u_id = 0

    for user in user_data:
        if user["email"] == email:
            user["is_logged_in"] = True
            u_id = user["u_id"]

    return {'u_id': u_id, 'token': aux_common.encode_token({'u_id': u_id})}


def logout(token):
    '''
    ## DESCRIPTION ##
    Given an active token, invalidates the token to log the user out. If a valid
    token is given, and the user is successfully logged out, it returns true,
    otherwise false.

    ## TYPES ##
    token - string

    ## RETURN VALUE ##
    {is_success}

    ## EXCEPTIONS ##
    N/A
    '''

    global user_data

    if aux_common.decode_token(token) == {'u_id': 'error_invalid_token'}:
        return {'is_success': False}

    for user in user_data:
        if user["u_id"] == aux_common.decode_token(token)["u_id"]:
            user["is_logged_in"] = False

    return {'is_success': True}


def passwordreset_request(email):
    '''
        ## DESCRIPTION ##
        Given an email, sends an email with a secret code, which, when entered in passwordreset/reset, shows the user
        trying to reset the password is the one who got the email.

        The secret code is generated by a random number generator, which is then stored in the corresponding user's
        dictionary in user_data.

        ## TYPES ##
        email - string

        ## RETURN VALUE ##
        {}

        ## EXCEPTIONS ##
        InputError if
            - Email provided is not associated with a user
            - Could not connect to SMTP server
    '''

    user_index = 0
    for user in user_data:
        if user["email"] == email:
            break
        user_index += 1
    if user_index >= len(user_data):
        raise InputError(description="That email is not associated with a user.")

    # Cryptographically secure random 8 digit number
    code = random.SystemRandom().randint(10000000, 99999999)

    # Set reset code in database
    user_data[user_index]['reset_code'] = code

    # Variables setup
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your password reset code for Slackr"
    message["From"] = "goodmemesslackr@gmail.com"
    message["To"] = email

    message_plain = f"""\
    Hi, {user_data[user_index]['first_name']}!
    
    Someone (hopefully you) requested a password reset for the account associated with this email.
    Slackr user handle: {user_data[user_index]['handle']}

    The code to reset the password is {code}.

    Please enter this code on the password reset page.
    
    If you did not request this change, you do not need to do anything.

    Regards,
    goodmemes Slackr team.
    """

    message_html = f"""\
        <html>
            <body>
                <p> Hi, {user_data[user_index]['first_name']}! </p>
                <p> Someone (hopefully you) requested a password reset for the account associated with this email. </p>
                <p> Slackr user handle: {user_data[user_index]['handle']} </p>
        
                <p> <b> The code to reset the password is {code}.</b> </p>

                <p> Please enter this code on the password reset page. </p>

                <p> If you did not request this change, you do not need to do anything. </p>
        
                <p> Regards, <br>
                goodmemes Slackr team.</p>
            </body>
        </html>
        """

    message.attach(MIMEText(message_plain, "plain"))
    message.attach(MIMEText(message_html, "html"))

    ctxt = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctxt) as server:
            server.login("goodmemesslackr@gmail.com", "kLXpDYUbo87B")
            server.sendmail("goodmemesslackr@gmail.com", email, message.as_string())
    except:
        raise InputError("Error occurred while sending reset email.")

    return {}


def passwordreset_reset(reset_code, new_password):
    try:
        reset_code = int(reset_code)
    except ValueError:
        raise InputError(description="Invalid reset code.")

    u_index = 0
    for user in user_data:
        curr_code = user.get('reset_code')
        if curr_code == reset_code:
            break
        u_index += 1
    if u_index >= len(user_data):
        raise InputError(description="Invalid reset code.")

    user_data[u_index]['password'] = new_password
    user_data[u_index].pop('reset_code')
    return {}



