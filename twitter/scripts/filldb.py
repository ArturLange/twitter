from sqlalchemy.orm import sessionmaker
from twitter import Base
from twitter.models import User


def fill_db(engine):
    session = sessionmaker(bind=engine)
    clear_database(engine)
    fill_users(session())


def clear_database(engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def fill_users(session):
    for i in range(5):
        user = User(username='user{}'.format(i), email='user{}@gmail.com'.format(i), password='pass')
        session.add(user)
    admin = User(username='admin', password='pass', email="admin@gmail.com", is_admin=True, name='Ahmed')
    session.add(admin)
    session.commit()
