import requests
from flask import Blueprint, request, session, redirect, render_template, url_for, flash, json

from tridents import db, app
from tridents.forms import ContactForm
from tridents.models import Post, ContactMessage

home = Blueprint('home', __name__)


@home.route('/')
def landing_page():
    return render_template('splash.html')


@home.route('/home')
def home():
    posts_list = Post.query.order_by(Post.publish_date.desc()).limit(10).all()
    user = session.get('profile')
    return render_template('home.html', user=user, posts=posts_list)


@home.route('/contact', methods=['GET', 'POST'])
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

    return render_template('contact.html', form=form, user=session.get('profile'))


@home.route('/callback')
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
