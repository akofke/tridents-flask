from flask import Flask, request, jsonify, session, redirect, render_template, url_for, logging

import os
import json
import requests


# create the application instance
app = Flask(__name__)

# load config from this file
app.config.from_object(__name__)

# default config
app.config.update(
    SECRET_KEY="development key",
    AUTH0_CALLBACK_URL="http://localhost:5000/callback"
)

# load additional config from the file at FLASK_CONFIG
app.config.from_envvar('FLASK_CONFIG', silent=False)


@app.route('/callback')
def callback():
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(domain=app.config.get('AUTH0_CLIENT_DOMAIN'))

    token_payload = {
        'client_id': app.config.get('AUTH0_CLIENT_ID'),
        'client_secret': app.config.get('AUTH0_CLIENT_SECRET'),
        'redirect_uri': app.config.get('AUTH0_CALLBACK_URL'),
        'code': code,
        'grant_type': 'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()
    print(token_info)

    user_url = "https://{domain}/userinfo?access_token={access_token}"\
        .format(domain=app.config.get('AUTH0_CLIENT_DOMAIN'), access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    session['profile'] = user_info

    return redirect(url_for('home'))


@app.route('/')
def landing_page():
    return render_template('splash.html')


@app.route('/home')
def home():
    return render_template('home.html', user=session.get('profile'))


@app.route('/logout')
def logout():
    session.pop('profile')
    return redirect(url_for('home'))




