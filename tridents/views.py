from functools import wraps

from flask import request, session, redirect, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired

from tridents import app, db
from tridents.models import Post, ContactMessage

import json
import requests
import arrow


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('home')
        return f(*args, **kwargs)

    return decorated


@app.template_filter('datetimeformat')
def datetimeformat(value: arrow.Arrow, format='%H:%M %m/%d/%Y'):
    return value.to('US/Eastern').strftime(format)


@app.route('/callback')
def callback():
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(domain=app.config.get('AUTH0_DOMAIN'))

    token_payload = {
        'client_id': app.config.get('AUTH0_CLIENT_ID'),
        'client_secret': app.config.get('AUTH0_CLIENT_SECRET'),
        'redirect_uri': url_for('callback', _external=True),
        'code': code,
        'grant_type': 'authorization_code'
    }

    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()

    user_url = "https://{domain}/userinfo?access_token={access_token}" \
        .format(domain=app.config.get('AUTH0_DOMAIN'), access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()
    print(user_info)

    session['profile'] = user_info

    return redirect(url_for('home'))


@app.route('/')
def landing_page():
    return render_template('splash.html')


@app.route('/home')
def home():
    posts_list = Post.query.limit(10).all()
    user = session.get('profile')
    return render_template('home.html', user=user, is_officer=is_officer(user), posts=posts_list)


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


class PostForm(FlaskForm):
    title = StringField('Title or Subject', validators=[DataRequired()])
    body = TextAreaField('Post', validators=[DataRequired()])


@requires_auth
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if not is_officer(session.get('profile')):
        return redirect('home')

    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            session.get('profile').get('name'),
            form.title.data,
            form.body.data
        )

        db.session.add(post)
        db.session.commit()

        flash('Post created successfully.', 'is-success')
        return redirect(url_for('posts'))

    return render_template('posts.html', form=form)


@app.route('/messages')
def messages():
    if not is_officer(session.get('profile')):
        return redirect('home')

    messages_list = ContactMessage.query.all()
    return render_template('messages.html', messages=messages_list)


def is_officer(user):
    if user and 'roles' in user:
        return 'officer' in user.get('roles')
    else:
        return False
