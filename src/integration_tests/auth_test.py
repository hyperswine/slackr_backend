import pytest
from main.error import InputError
import app.auth as auth

# Test everything works OK for valid input
def test_register_basic1():
    results = auth.register('validemail123@gmail.com', 'password123!!', 'Donald', 'Trumpou')
    assert type(results) is dict
    assert type(results['u_id']) is int
    assert type(results['token']) is str

def test_register_basic2():
    results = auth.register('valid.email123@gmail.com', 'VeRYLegalANDvErYC00L123', 'Donaldo', 'Trump')
    assert type(results) is dict
    assert type(results['u_id']) is int
    assert type(results['token']) is str

# Test with no personal info
def test_register_invalid_email1():
    with pytest.raises(InputError):
        auth.register('@gmail.com', 'password', 'John', 'Citizen')
    
# Test with no domain       
def test_register_invalid_email2():
    with pytest.raises(InputError):
        auth.register('john@', 'password', 'John', 'Citizen') 
        
def test_register_invalid_email3():
    with pytest.raises(InputError):
        auth.register('john.com', 'password', 'John', 'Citizen')                 

# Test with empty email string
def test_register_empty_email():
    with pytest.raises(InputError):
        auth.register('', 'password', 'John', 'Citizen')    

# Test with less than 6 character password
def test_register_invalid_password():
     with pytest.raises(InputError):
        auth.register('john.citizen@gmail.com', '1234', 'John', "Citizen")

# Test that everything works when 6 character password is used
def test_register_password_just_long_enough():
    results = auth.register('john.citizen1241@gmail.com', '123456', 'John', "Citizen")
    assert type(results) is dict
    assert type(results['u_id']) is int
    assert type(results['token']) is str        

# Test with first name over 50 characters
def test_register_first_name_length1():
    with pytest.raises(InputError):
        auth.register('john.citizen1@gmail.com', 'password', 'a' * 51, 'Citizen')

# Test with first name just short enough
def test_register_first_name_length2():
    results = auth.register('john.citizen2@gmail.com', 'password', 'a' * 50, 'Citizen')
    assert type(results) is dict
    assert type(results['u_id']) is int
    assert type(results['token']) is str

# Test with less than one first name character
def test_register_first_name_length3():
    with pytest.raises(InputError):
        auth.register('john.citizen3@gmail.com', 'password', '', 'Citizen')

# Test with first name just long enough 
def test_register_first_name_length4():
    results = auth.register('john.citizen251@gmail.com', 'password', 'A', 'Citizen')
    assert type(results) is dict
    assert type(results['u_id']) is int
    assert type(results['token']) is str

# Test with last name over 50 characters
def test_register_last_name_length1():
    with pytest.raises(InputError):
        results = auth.register('john.citizen2151@gmail.com', 'password', 'John', 'a' * 51)
        
# Test with first name just short enough
def test_register_last_name_length2():
    results = auth.register('john.citizen21521@gmail.com', 'password', 'John', 'a' * 50)
    assert type(results) is dict
    assert type(results['u_id']) is int
    assert type(results['token']) is str

# Test with less than one last name character
def test_register_last_name_length3():
    with pytest.raises(InputError):
        results = auth.register('john.citizen23462@gmail.com', 'password', 'John', '')

# Test with just enough last name characters
def test_register_last_name_length4():
    results = auth.register('john.citizen23463262@gmail.com', 'password', 'John', 'C')
    assert type(results) is dict
    assert type(results['u_id']) is int
    assert type(results['token']) is str

# Test email already being used
def test_register_used_email_test():
    auth.register('john.citizen32452332@gmail.com', 'password', 'John', 'Citizen')
    with pytest.raises(InputError):
        auth.register('john.citizen32452332@gmail.com', 'password', 'John', 'Citizen')

# Test email already being used (name doesn't match)
def test_register_used_email_test2():
    auth.register('john.citizen324523321@gmail.com', 'password', 'John', 'Citizen')
    with pytest.raises(InputError):
        auth.register('john.citizen324523321@gmail.com', 'password2', 'John2', 'Citizen2')

# Test email already being used (multiple users)
def test_register_used_email_test3():
    auth.register('john.citizen@gmail234524.com', 'password', 'John', 'Citizen')
    auth.register('john.citizen21213213213@gmail.com', 'password2', 'John2', 'Citizen2')
    with pytest.raises(InputError):
        auth.register('john.citizen21213213213@gmail.com', 'password', 'John', 'Citizen')


# Test if login works by comparing id from login top when it was created during registration
# Assumes auth register works 
def test_login_test1():
    results1 = auth.register('john.citizea@gmail.com', 'password', 'John', 'Citizen')
    id1 = results1['u_id']
    
    results2 = auth.login('john.citizea@gmail.com', 'password')
    id2 = results2['u_id']
    
    assert id1 == id2
    assert type(results2) is dict
    assert type(results2['u_id']) is int
    assert type(results2['token']) is str
    
# Test with incorrect password    
def test_login_test2():
    auth.register('john.citizeb@gmail.com', 'password', 'John', 'Citizen')
    with pytest.raises(InputError):
        auth.login('john.citizeb@gmail.com', '12345678')

# Test with incorrect password (multiple users, wrong user's password) 
def test_login_test3():
    auth.register('john.citizel@gmail.com', 'password', 'John', 'Citizen')
    auth.register('john2.citizel2@gmail.com', '12345678', 'John2', 'Citizen2')
    with pytest.raises(InputError):
        auth.login('john.citizel@gmail.com', '12345678')

# Test with invalid email input
def test_login_invalid_email_test1():
    with pytest.raises(InputError):
        auth.login('@gmail.com', 'password')
        
def test_login_invalid_email_test2():
    with pytest.raises(InputError):
        auth.login('john.gmail.com', 'password')      
        
def test_login_invalid_email_test3():
    with pytest.raises(InputError):
        auth.login('john.com', 'password')          

# Logging in with un registered email
def test_login_unseen_email_test():
    with pytest.raises(InputError):
        auth.login('john.citizen@gmail.com', 'password')   

# If a valid token is given, and the user is successfully logged out, it returns true
def test_logout_test1():
    results1 = auth.register('john.citizen@gmail.com', 'password', 'John', 'Citizen')
    results2 = auth.logout(results1['token'])
    
    assert results2['is_success'] == True
 
# Returns False if invalid token is given   
def test_logout_test2():
    results1 = auth.register('john.citizen6969@gmail.com', 'password', 'John', 'Citizen')
    results1['token'] = 'INVALID_TOKEN'
    results2 = auth.logout(results1['token'])
    
    assert results2['is_success'] == False    
