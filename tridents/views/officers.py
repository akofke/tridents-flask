from flask import session, redirect, flash, url_for, render_template, Blueprint

from tridents import db
from tridents.forms import PostForm
from tridents.models import Post, ContactMessage

officers = Blueprint('officers', __name__)


@officers.route('/posts', methods=['GET', 'POST'])
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

    return render_template('posts.html', form=form, user=session.get('profile'))


@officers.route('/messages')
def messages():
    if not is_officer(session.get('profile')):
        return redirect('home')

    messages_list = ContactMessage.query.all()
    return render_template('messages.html', messages=messages_list, user=session.get('profile'))


def is_officer(user):
    if user and 'roles' in user:
        return 'officer' in user.get('roles')
    else:
        return False
