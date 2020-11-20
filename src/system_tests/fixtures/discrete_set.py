'''
This is the discrete set of functions and fixtures to use in system_testing.
'''
import app.auth as auth
import aux_.common as aux_common
import main.data as data
import app.channels as channels

logged_in_users = []


def register_users(n):
    '''
    register n people, who automatically become logged in.
    '''
    logged_in_users.append([auth.register(
        f"legit{i}@gmail.com", "1r1fapfoj", "Nuttus", "Longinus") for i in range(n)])


#@pt.fixture
def valid_package_register():
    '''
    Returns a dict containing email, password, first name, last name.
    '''

    email_ = "today_is_the_day@gmail.com"
    password_ = "WR1241jfasf"
    name_first = "Alcholus"
    name_last = "Drinkus"

    return {"email": email_, "password": password_, "name_first": name_first,
            "name_last": name_last}


def logout_users():
    '''
    Logout all users in logged_in_users.
    '''
    map(lambda a: auth.logout(a["token"]), logged_in_users)
    # just need them to be registered, so dont clear workspace from logout onwards.


def create_first_channel(k):
    '''
    Creates a channel and returns it channel_id.

    Uses the user[k] user in [user_data] as the authorized caller and hence the owner.

    Return value = {"channe_id", "token"}
    '''
    token_owner_channel = aux_common.encode_token(data.user_data[k]["u_id"])
    ch_id = channels.create(token_owner_channel, "FOX_NEWS", True)

    return {"channel_id": ch_id["channel_id"], "token": token_owner_channel}


def reset_data(data_t):
    '''
    Input - The data field in data.py that you want to delete.
    NOTE: data_t must be the global variable which you pass into the function.

    Given a specific field in data.py, reset the data.

    Output - True on success.
    '''
    data_t.clear()

    if data_t != {}:
        raise Exception(f'Could not reset {data_t}')

    return True
