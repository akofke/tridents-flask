from datetime import datetime

from tridents import db


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)

    def __init__(self, author, title, body):
        self.author = author
        self.title = title
        self.body = body
        self.publish_date = datetime.utcnow()

    def __repr__(self):
        return '<Post {}>'.format(self.title)