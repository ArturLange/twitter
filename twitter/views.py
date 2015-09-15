from pyramid.view import view_config

from twitter import DBSession
from twitter.models import User


@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    return {'project': 'twitter'}


@view_config(route_name='account', renderer='templates/account.pt')
def account_view(request):
    user = DBSession.query(User).filter(User.id == 1).first()
    return {'user': user}


@view_config(route_name='post_view', renderer='templates/home.pt')
def post_view(request):
    return {'project': 'twitter'}
