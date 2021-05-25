"""Models for Blogly."""
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                        nullable=False)
    last_name = db.Column(db.String(50),
                        nullable=True)
    img_url = db.Column(db.String(100),
                        nullable=True)


class Post(db.Model):

    __tablename__ = "posts"

    id =  db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(100))
    created_at = db.Column(db.DateTime,default=datetime.datetime.now())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE'))

    user = db.relationship('User',backref='posts')

    tags = db.relationship('Tag',secondary='posttags',backref='posts')



class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    name = db.Column(db.Text,unique=True)

class PostTag(db.Model):

    __tablename__ = "posttags"

    post_id = db.Column(db.Integer,db.ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True)

    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id',ondelete='CASCADE'),primary_key=True)
