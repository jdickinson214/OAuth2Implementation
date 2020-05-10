# #from google.cloud import datastore

# from flask import Flask, request, redirect
# from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin)
# import json
# import requests
# import oauthSettings


# app = Flask(__name__)
# app.config.from_pyfile('oauth.py')

# @app.route("/")
# def welcome():
#     return "Welcome! Go to link to test Oauth 2.0: " + oauthSettings.testURL

# @app.route("/oauth")
# def oath_test():
#     secret = oauthSettings.generate_api_secret


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8080, debug=True)


import json
import flask
import requests


app = flask.Flask(__name__)

CLIENT_ID = '123456789.apps.googleusercontent.com'
CLIENT_SECRET = 'abc123'  # Read from a file or environmental variable in a real app
SCOPE = 'https://www.googleapis.com/auth/drive.metadata.readonly'
REDIRECT_URI = 'http://example.com/oauth2callback'


@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = json.loads(flask.session['credentials'])
  if credentials['expires_in'] <= 0:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
    req_uri = 'https://www.googleapis.com/drive/v2/files'
    r = requests.get(req_uri, headers=headers)
    return r.text


@app.route('/oauth2callback')
def oauth2callback():
  if 'code' not in flask.request.args:
    auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
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
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()