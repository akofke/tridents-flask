from flask import Flask, request, jsonify, session, redirect, render_template, url_for

import os
import json
import requests


# create the application instance
app = Flask(__name__)

# load config from this file
app.config.from_object(__name__)

# default config
app.config.update(
    SECRET_KEY="development key"
)

# load additional config from the file at FLASK_CONFIG
app.config.from_envvar('FLASK_CONFIG', silent=True)


@app.route('/callback')
def callback_handling():
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(domain=app.config.get('AUTH0_CLIENT_DOMAIN'))

    token_payload = {
        'client_id': app.config.get('AUTH0_CLIENT_ID'),
        'client_secret': app.config.get('AUTH0_CLIENT_SECRET'),
        'redirect_uri': url_for('callback_handling'),
        'code': code,
        'grant_type': 'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()

    user_url = "https://{domain}/userinfo?access_token={access_token}"\
        .format(domain=app.config.get('AUTH0_CLIENT_DOMAIN'), access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    session['profile'] = user_info

    return redirect(url_for('/home'))


@app.route('/home')
def home():
    return render_template('home.html', user=session.get('profile'))


