from datetime import datetime

import re
import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.password import PasswordType
import transaction
from twitter import Base, DBSession

follows = sa.Table('follows', Base.metadata,
                   sa.Column('follower_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
                   sa.Column('followed_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
                   )


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Unicode, nullable=False, unique=True)
    name = sa.Column(sa.Unicode)
    email = sa.Column(sa.Unicode, nullable=False, unique=True)
    password = sa.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    is_admin = sa.Column(sa.Boolean, default=False)
    followers = relationship("User", secondary=follows, primaryjoin=id == follows.c.followed_id,
                             secondaryjoin=id == follows.c.follower_id, backref='followed')

    def __init__(self, username, email, password, name='', is_admin=False):
        self.username = username
        self.name = name
        self.email = email.lower()
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return str(dict(username=self.username, email=self.email))

    @classmethod
    def get_by_email(cls, request, email):
        query = request.db.query(cls)
        email = email if email is not None else ''
        by_email = func.lower(cls.email) == email.lower()
        return query.filter(by_email).first()

    @classmethod
    def get_by_username(cls, request, username):
        query = request.db.query(cls)
        username = username if username is not None else ''
        by_username = cls.username == username
        return query.filter(by_username).first()


posts_hashtags = sa.Table('posts_hashtags', Base.metadata,
                          sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id')),
                          sa.Column('hashtag_id', sa.Integer, sa.ForeignKey('hashtags.id'))
                          )


class Post(Base):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer, primary_key=True)
    date_created = sa.Column(sa.types.DateTime, nullable=False)
    creator_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    original_creator_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    content = sa.Column(sa.Text)
    hashtags = relationship('Hashtag', secondary=posts_hashtags, backref='posts')

    creator = relationship('User', backref='posts',
                           primaryjoin="Post.creator_id == User.id")
    original_creator = relationship('User', primaryjoin="Post.original_creator_id == User.id")

    def __init__(self, original_creator_id, content, creator_id=None):
        self.content = content
        self.date_created = datetime.now()
        self.original_creator_id = original_creator_id
        self.creator_id = creator_id if creator_id else original_creator_id
        hashtags = re.findall(r"#[\w]+", content)
        names = [hashtag[1:] for hashtag in hashtags]
        with transaction.manager:
            for name in names:
                hashtag = DBSession.query(Hashtag).filter(Hashtag.name == name).first()
                if hashtag is None:
                    hashtag = Hashtag(name)
                    self.hashtags.append(hashtag)
                else:
                    self.hashtags.append(hashtag)

    @classmethod
    def get_by_hashtag(cls, request, hashtag):
        query = request.db.query(cls)
        by_hashtag = cls.hashtags.contains(hashtag)
        return query.filter(by_hashtag).all()

    @classmethod
    def get_by_creator(cls, request, creator):
        query = request.db.query(cls)
        by_creator = cls.creator == creator
        return query.filter(by_creator).all()


class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_name(cls, request, name):
        query = request.db.query(cls)
        by_name = cls.name == name
        return query.filter(by_name).first()
