from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __table_name__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    comments = db.relationship('Comment')
    posts = db.relationship('Post')
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.password = self.__create_password(password)
        self.email = email

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model):
    __table_name__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posts_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    text = db.Column(db.Text())
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)


class Post(db.Model):
    __table_name__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posts = db.relationship('Comment')
    title = db.Column(db.String(60))
    content = db.Column(db.Text())
    imagen = db.Column(db.Text(), default='None.jpg')
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
