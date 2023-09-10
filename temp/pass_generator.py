import random

lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = lowercase.upper()
numbers = '0123456789'
symbols = '!@#$%&?'

user_defined_chars = ''

source = [lowercase, uppercase, numbers, symbols]

def generate_password(length):
    password = ''
    for x in range(length):
        guess = random.choice(source)
        password += random.choice(guess)
    return password

def ask_user():
    global user_defined_chars
    user_defined_chars = input('How many characters? ')
    test_input()

def test_input():
    try:
        int(user_defined_chars)
        is_num = True
    except ValueError:
        is_num = False

    if is_num:
        print(generate_password(int(user_defined_chars)))
    else:
        print('Please enter a number... ')
        ask_user()

ask_user()
