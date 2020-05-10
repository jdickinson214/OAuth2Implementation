import requests
import random
import string

CLIENT_SECRETS_FILE = "../../hw6-dickinsj-9efa36001a38.json"


testURL = "http://127.0.0.1:8080/oauth"

def generate_api_secret(stateLength=10):
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars) for i in range(stateLength)))
    






#GET 
#https://accounts.google.com/o/oauth2/v2/auth

#response_type:code


#client_id:[your-client-id]
#redirect_uri:[where-the-client-gets-redirected-to]
#scope:[list-of-scopes]
#state:[random-secret-string]


