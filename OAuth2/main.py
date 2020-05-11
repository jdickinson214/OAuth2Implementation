import json
import flask
import requests
import random_function as rc
import os

app = flask.Flask(__name__, static_url_path='', static_folder='web/static')

#gcp gets angry if this is not present
app.secret_key = str(rc.generate_random_code(20))

#get client_secret file from directory and assign values
client_secret_path = os.path.dirname(os.path.abspath(__file__)) + "/creds/client_secret.json"
CLIENT_SECRET_FILE = json.load(open(client_secret_path))
CLIENT_ID = CLIENT_SECRET_FILE['web']['client_id']
CLIENT_SECRET = CLIENT_SECRET_FILE['web']["client_secret"]
SCOPE = 'email profile'
REDIRECT_URI = 'https://hw6-dickinsj2.uc.r.appspot.com/oauth2callback'
#for testing only
#REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'

@app.route('/welcome')
def welcome():
    return app.send_static_file('welcome.html')

#####################################################################################
# new user flow:    
#   redirect to /oauth2callback
#   generate state and store in session
#   redirect user to google with proper params (state included), user consents access
#   get code back from google which redirects back to oauth2callback
#   check that state is present and matches original state 
#   send a post to googleapis.com/token from client with all credentials
#   get back token, store in session, redirect back to index page
#   ensure creds in place, use token to access user data from google
#   format and display to user
#####################################################################################

@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = json.loads(flask.session['credentials'])
  if 'expires_in' not in credentials:
    return flask.redirect(flask.url_for('oauth2callback'))
  if credentials['expires_in'] <= 0:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    headers = {'Authorization': 'Bearer {}'.format(
        credentials['access_token'])}
    req_uri = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses'
    r = requests.get(req_uri, headers=headers)
    res = json.loads(r.text)
    if 'state' not in flask.session:
        return 'state not in session'
    userInfo = {'first name': res["names"][0]["givenName"],
                'last name': res['names'][0]['familyName'],
                'email': res['emailAddresses'][0]['value'],
                'state': flask.session['state']}
    return json.dumps(userInfo)


@app.route('/oauth2callback')
def oauth2callback():
  if 'code' not in flask.request.args or 'state' not in flask.session:
    state = rc.generate_random_code(10)
    auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                '&client_id={}&redirect_uri={}&scope={}&state={}&prompt=consent').format(CLIENT_ID, REDIRECT_URI, SCOPE, state)
    flask.session['state'] = state
    return flask.redirect(auth_uri)
  else:
    if flask.session['state'] != flask.request.args.get('state'):
        return "States do not match"  
    auth_code = flask.request.args.get('code')
    data = {'code': auth_code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'}
    r = requests.post('https://oauth2.googleapis.com/token', data=data)
    flask.session['credentials'] = r.text
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
  app.debug = True
  app.run()
