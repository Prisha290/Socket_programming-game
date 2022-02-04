import uuid
import hashlib


# generate hashed password
def hash_password(password):
    salt = uuid.uuid4().hex
    code = salt.encode() + password.encode()
    hashed_str = hashlib.sha256(code).hexdigest() + ':' + salt
    return hashed_str


# check correctness
def check_password(hashed_psd, user_input_psd):
    flag = False
    password, salt = hashed_psd.split(':')
    if hashlib.sha256(salt.encode() + user_input_psd.encode()).hexdigest() == password:
        flag = True
    return flag


if __name__ == "__main__":
    # create a new hashed password
    psd = input('Enter a password: ')
    hashed_pwd = hash_password(psd)
    print('Sha256: ' + hashed_pwd)

    # check if the password matches with database
    user_input = input('Enter your password to check: ')
    if check_password(hashed_pwd, user_input):
        print('You entered the right password')
    else:
        print('The password does not match')
