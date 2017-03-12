from flask import request, session, redirect, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired

from tridents import app, db
from tridents.models import Post, ContactMessage

import json
import requests
import arrow

@app.template_filter('datetimeformat')
def datetimeformat(value: arrow.Arrow, format='%H:%M %d/%m/%Y'):
    return value.to('US/Eastern').strftime(format)


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

    user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain=app.config.get('AUTH0_CLIENT_DOMAIN'), access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    session['profile'] = user_info

    return redirect(url_for('home'))


@app.route('/')
def landing_page():
    return render_template('splash.html')


@app.route('/home')
def home():
    posts = Post.query.limit(10).all()
    return render_template('home.html', user=session.get('profile'), posts=posts)


@app.route('/logout')
def logout():
    session.pop('profile')
    return redirect(url_for('home'))


class ContactForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    sender = StringField('Your Name')
    reach_at = StringField('Email or Phone Number')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        message = ContactMessage(
            form.message.data,
            form.sender.data if form.sender.data != '' else None,
            form.reach_at.data if form.reach_at.data != '' else None
        )

        db.session.add(message)
        db.session.commit()

        flash('Message sent successfully. Thank you!', 'is-success')
        return redirect(url_for('home'))

    return render_template('contact.html', form=form)

