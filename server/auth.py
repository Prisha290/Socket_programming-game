"""
This python script is used to generate hashed passwords
and check correctness of passwords.
"""
import hashlib
import json
import re
import uuid

USERS_FILE = 'users.json'

# [CLIENT] This function generates a hashed password

def hash_password(password):
    salt = uuid.uuid4().hex
    code = salt.encode() + password.encode()
    hashed_str = hashlib.sha256(code).hexdigest() + ':' + salt
    return hashed_str


# [SERVER] This password checker function checks if the password is correct
def check_hash_password(hashed_psd, user_input_psd):
    flag = False
    password, salt = hashed_psd.split(':')
    if hashlib.sha256(salt.encode() + user_input_psd.encode()).hexdigest() == password:
        flag = True
    return flag


# [CLIENT] Check if username is valid
def check_username(username):
    flag = False
    if username.isalpha() and len(username) >= 3:
        flag = True
    return flag


# [CLIENT] Check if password is valid
def check_password(password):
    # Regex for password
    reg = "^(?=.*[a-z]){0,}(?=.*[A-Z]){0,}(?=.*\d){0,}(?=.*[@$!%*#?&]){0,}[A-Za-z\d@$!#%*?&]{4,18}$"
    # Compiling regex
    match_re = re.compile(reg)
    reg_result = match_re.search(password)
    flag = False
    if reg_result:
        flag = True
    return flag


# [SERVER] Check if user exist in users.json
def check_user_exist(username):
    flag = False
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
        for user in users:
            if user['username'] == username:
                flag = True
    return flag


# [SERVER] Check if user password is correct
def check_user_password(username, password):
    flag = False
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
        for user in users:
            if user['username'] == username and check_hash_password(user['password'], password):
                flag = True
    return flag


# [SERVER] Add user to users.json
def add_user(username, password):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    user = {
        'username': username,
        'password': hash_password(password)
    }
    users.append(user)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
