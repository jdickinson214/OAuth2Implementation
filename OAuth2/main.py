import json
import flask
import requests
import oauthSettings as OA

app = flask.Flask(__name__)

CLIENT_ID = "489568071894-209q40tq61bg69s3efg1nr9jho98fn7q.apps.googleusercontent.com"
CLIENT_SECRET = "vI4P_eVHQ8zPuZRthsM0V8GR"
SCOPE = 'email profile'
REDIRECT_URI = 'https://hw6-dickinsj2.uc.r.appspot.com/oauth2callback'
#REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'


@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = json.loads(flask.session['credentials'])
  if credentials['expires_in'] <= 0:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    headers = {'Authorization': 'Bearer {}'.format(
        credentials['access_token'])}
    req_uri = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses'
    r = requests.get(req_uri, headers=headers)
    res = json.loads(r.text)
    #return r.text
    userInfo = {'first name': res["names"][0]["givenName"],
                'last name': res['names'][0]['familyName'],
                'email': res['emailAddresses'][0]['value'],
                'state': flask.session['state']}
    return json.dumps(userInfo)


@app.route('/oauth2callback')
def oauth2callback():
  if 'code' not in flask.request.args:
    state = OA.generate_state()
    auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                '&client_id={}&redirect_uri={}&scope={}&state={}&prompt=consent').format(CLIENT_ID, REDIRECT_URI, SCOPE, state)
    flask.session['state'] = state
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    data = {'code': auth_code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'}
    r = requests.post('https://oauth2.googleapis.com/token', data=data)
    flask.session['credentials'] = r.text
    if flask.session['state'] != flask.request.args.get('state'):
        return "States do not match"
    return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()
