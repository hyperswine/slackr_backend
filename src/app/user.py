'''
Core user and users functions.

Pylint disable justifications:
no-name-in-module and import-error:
    Since pylint is run from user.py, but we run the server from server.py, there will be
    import errors by pylint because sys.path does not contain src/ like it should
global-statement and invalid-name:
    The assignment recommends using global variables for data storage.
'''
# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=global-statement
# pylint: disable=invalid-name

from main.data import user_data, next_id
from io import BytesIO
from PIL import Image, ImageTk, UnidentifiedImageError
import requests
from main.error import AccessError, InputError
import aux_.common as aux_common
import aux_.discrete as aux_discrete
import urllib.request

# For valid check email

# user_data = the list of users in the channel


def profile(token, u_id):
    """

    INPUTS: token, u_id

    DESCRIPTION: For a valid user, Returns information about their user id, email
    first name last name and handle

    RETURNS: { user }

    INPUTERROR:
        * User with u_id is not a valid user
    """
    if aux_common.decode_token(token) == {'u_id': 'error_invalid_token'}:
        raise AccessError(description="Invalid token")
    # Input Error
    if not aux_discrete.user_exists(u_id):
        raise InputError(description=f'User with u_id {u_id} is not valid')

    # Loop through all the users and return the right user through its identifiers (u_id)
    for user in user_data:
        if user['u_id'] == u_id:
            # check if i have the layout of the dictionary plss
            return {
                'user':
                    {'u_id': user['u_id'],
                     'email': user['email'],
                     'name_first': user['first_name'],
                     'name_last': user['last_name'],
                     'handle_str': user['handle'],
                     'profile_img_url': user['profile_img_url']
                     }  # Need to add handle_str to the global data
            }
    return {}


def setname(token, first_name, last_name):
    """

    INPUTS:token, name_first,name_last

    RETURNS: {}

    INPUTERROR:
        * Name_first is not between 1 and 50 charactors inclusive in length
        * Name_last is not between 1 and 50 characters inclusive in length

    DESCRIPTION: Updates the authorised user's first and last name

    """
    global user_data
    # Raise errors first

    if len(first_name) >= 50 or len(first_name) <= 1:
        raise InputError(
            description='Length of first name must be between 1 - 50 characters')

    if len(last_name) >= 50 or len(last_name) <= 1:
        raise InputError(
            description='Length of last name must be between 1 - 50 characters')

      # decode token to get user_id, assuming u_id is the identifier for the user_data
    if aux_common.decode_token(token) == {'u_id': 'error_invalid_token'}:
        raise AccessError(description="Invalid token")

    # Reveals dictionary of form {"u_id": u_id}
    user_id = aux_common.decode_token(token)
    # remember user_id is a dictionary of 'u_id'
    # Go into that users dictionary and change the first_name and last_name to inputs

    for user in user_data:
        if user['u_id'] == user_id['u_id']:
            user['first_name'] = first_name
            user['last_name'] = last_name

    return {}


def setemail(token, email):
    """
    INPUTS: token, email

    RETURNS: {}

    INPUTERROR:
        *Email not valid (Copy code)
        *Already in use
    DESCRIPTION:
        Updates authorised user's email address
    """
    global user_data

    if not aux_discrete.check_email_valid(email):
        raise InputError(description='Email is not of valid form')

    if not aux_discrete.check_email_in_use(email):
        raise InputError(description='Email already in use')

    if aux_common.decode_token(token) == {'u_id': 'error_invalid_token'}:
        raise AccessError(description="Invalid token")

    user_id = aux_common.decode_token(token)

    for user in user_data:
        if user['u_id'] == user_id['u_id']:
            user['email'] = email
    return {}


def sethandle(token, handle_str):
    """
    INPUTS: token, handle_str
    RETURNS: {}

    INPUTERROR:
        *2 <= handle_str <= 20
        * handle already used
    DESCRIPTION: Updates an AUTHORISED user's handle
    """
    global user_data
    if len(handle_str) >= 20 or len(handle_str) <= 1:
        raise InputError(
            description='Handle string must be between 1 and 20 characters')
    if aux_discrete.check_handle_in_use is False:
        raise InputError(description='Handle string is already in use')

    if aux_common.decode_token(token) == {'u_id': 'error_invalid_token'}:
        raise AccessError(description="Invalid token")

    user_id = aux_common.decode_token(token)

    for user in user_data:
        if user['u_id'] == user_id['u_id']:
            user['handle'] = handle_str

    return {}


def all_(token):
    """
        Returns a list of all users and their associated details
    """
    # Loop through all users, and append to new dictionary and return that dictionary
    users_dictionary = {'users': []}
    if aux_common.decode_token(token) == {'u_id': 'error_invalid_token'}:
        raise AccessError(description="Invalid token")

    for user in user_data:
        user_dict = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['first_name'],
            'name_last': user['last_name'],
            'handle_str': user['handle'],
            'profile_img_url': user['profile_img_url']
        }
        # Appends dictionaries to the list
        users_dictionary['users'].append(user_dict)

    return users_dictionary


def upload_photo(token, img_url, x_start, y_start, x_end, y_end):
    '''
    INPUTS: token (str), img_url (str), x_start, y_start, x_end, y_end (ints)
    RETURNS: {}

    AUTHERROR: invalid token
    INPUTERROR:
        Image URL request raises status code not 200
        x_start, y_start, x_end, y_end are not in the dimensions of the image at the URL or are invalid
        Image URL is not linked to a valid image
        Image URL is not a JPEG/JPG file.

    DESCRIPTION: Updates an AUTHORISED user's handle
    '''
    global user_data, next_id

    try:
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)
    except ValueError:
        raise InputError(description="x & y values must be integers")

    u_id = aux_common.decode_token(token)['u_id']
    if u_id == "error_invalid_token":
        raise AccessError(description="Invalid token")
    response = requests.get(img_url)
    if response.status_code != 200:
        raise InputError(description=f"Image URL invalid: status code {response.status_code}")
    try:
        img = Image.open(BytesIO(response.content))
    except UnidentifiedImageError:
        raise InputError(description="That URL is not a direct link to an image")

    if img.format != "JPEG":
        raise InputError(description="Image must be a JPEG/JPG")

    width, height = img.size
    if x_start > width or x_end > width or y_start > height or y_end > height:
        raise InputError(description="One or more crop parameters were out of the photo's range.")
    try:
        img = img.crop((x_start, y_start, x_end, y_end))
    except SystemError:
        raise InputError(description="Crop parameters were invalid. Are the ends greater than the starts?")

    next_img_name = next_id.get('image_name')
    if not next_img_name:  # key does not exist yet
        next_id['image_name'] = 0
        next_img_name = 0

    try:
        img.save(f"./profile_images/{next_img_name}.jpg", "JPEG")
    except SystemError:
        raise InputError(description="Error occurred while saving the image. Are the ends greater than the starts?")

    u_index = aux_discrete.find_user(u_id)
    user_data[u_index]['profile_img_url'] = f"http://127.0.0.1:8080/profileimages/{next_img_name}.jpg"

    next_id['image_name'] += 1

    return {}
