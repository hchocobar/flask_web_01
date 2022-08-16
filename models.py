from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash  # genera un hash para encriptar el password
from werkzeug.security import check_password_hash  # verifica el hash de un password
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(103))  # 103 porque encriptamos la contraseña
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    comments = db.relationship('Comment')

    def __init__(self, username, password, email):
        self.username = username
        self.password = self.__create_password(password)
        self.email = email

    def __create_password(self, password):
        return generate_password_hash(password, salt_length=16)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeingnKey('users.id'))
    text = db.Column(db.Text())
    create_date = db.Column(db.DataTime, default=datetime.datetime.now)

