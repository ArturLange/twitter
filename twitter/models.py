import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.password import PasswordType

from twitter import Base


class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Unicode, nullable=False, unique=True)
    first_name = sa.Column(sa.Unicode)
    last_name = sa.Column(sa.Unicode)
    email = sa.Column(sa.Unicode, nullable=False, unique=True)
    password = sa.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    is_admin = sa.Column(sa.Boolean, default=False)
    posts = relationship("Post", backref="creator")

    def __init__(self, username, email, password, first_name='', last_name='', is_admin=False):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
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
    content = sa.Column(sa.Text)
    hashtags = relationship('Hashtag', secondary=posts_hashtags, backref='posts')

    def __init__(self, date_created, creator_id, content):
        self.content = content
        self.date_created = date_created
        self.creator_id = creator_id


class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode, nullable=False, unique=True)
