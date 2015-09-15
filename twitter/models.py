import sqlalchemy as sa
from sqlalchemy import func
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

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.password = password
        self.is_admin = is_admin

    @classmethod
    def get_by_email(cls, request, email):
        query = request.db.query(cls)
        email = email if email is not None else ''
        by_email = func.lower(cls.email) == email.lower()
        return query.filter(by_email).first()
