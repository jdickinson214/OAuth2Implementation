import requests
import random
import string

#input length parameter and get a string of random ascii letters and digits
#used for app.secret_key and for 'state' variable in OAuth2 main.py
def generate_random_code(stateLength=10):
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars) for i in range(stateLength)))
    
