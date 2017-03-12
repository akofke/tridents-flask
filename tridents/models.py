from datetime import datetime

import arrow
from sqlalchemy_utils import ArrowType

from tridents import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    publish_date = db.Column(ArrowType)

    def __init__(self, author, title, body):
        self.author = author
        self.title = title
        self.body = body
        self.publish_date = arrow.utcnow()

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80))
    reach_at = db.Column(db.String(80))
    message = db.Column(db.Text)
    send_date = db.Column(ArrowType)

    def __init__(self, message, sender=None, reach_at=None):
        self.sender = sender
        self.reach_at = reach_at
        self.message = message
        self.send_date = arrow.utcnow()

    def __repr__(self):
        return '<ContactMessage {}>'.format(self.send_date)