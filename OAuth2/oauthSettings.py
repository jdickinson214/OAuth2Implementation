import requests
import random
import string

def generate_random_code(stateLength=10):
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars) for i in range(stateLength)))
    
